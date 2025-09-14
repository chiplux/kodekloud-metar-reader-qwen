from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

def fetch_metar(station_id):
    """Fetch METAR data from aviationweather.gov API"""
    url = f"https://aviationweather.gov/api/data/metar?ids={station_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except Exception as e:
        return None

def decode_metar(metar_text):
    """Decode METAR text into plain English"""
    if not metar_text:
        return "Unable to fetch METAR data"
    
    # Parse basic elements
    parts = metar_text.split()
    
    # Extract station ID (first element should be station code)
    station_id = "Unknown"
    start_index = 0
    
    # Check if first element is METAR or SPECI (report type)
    if parts[0] in ["METAR", "SPECI"] and len(parts) > 1:
        station_id = parts[1]
        start_index = 1
    elif parts[0] not in ["METAR", "SPECI"]:
        station_id = parts[0]
        start_index = 0
    
    # Extract date/time (element after station ID)
    datetime = parts[start_index + 1] if len(parts) > start_index + 1 else "Unknown"
    day = datetime[:2] if len(datetime) >= 2 else "Unknown"
    time = datetime[2:6] if len(datetime) >= 6 else "Unknown"
    
    # Extract wind information
    wind_info = "Calm"
    for i in range(start_index + 2, len(parts)):
        part = parts[i]
        if re.match(r'^\d{3}\d{2}(?:G\d{2})?(?:KT|MPS|KMH)$', part):
            wind_dir = part[:3]
            wind_speed = part[3:5]
            gust = ""
            if 'G' in part:
                gust_start = part.find('G')
                gust = f" gusting to {part[gust_start+1:gust_start+3]} knots"
            
            # Convert wind direction to compass direction
            if wind_dir == "000":
                direction = "Calm"
            elif wind_dir == "VRB":
                direction = "Variable"
            else:
                wind_deg = int(wind_dir)
                if (338 <= wind_deg <= 360) or (0 <= wind_deg <= 22):
                    direction = "North"
                elif 23 <= wind_deg <= 67:
                    direction = "Northeast"
                elif 68 <= wind_deg <= 112:
                    direction = "East"
                elif 113 <= wind_deg <= 157:
                    direction = "Southeast"
                elif 158 <= wind_deg <= 202:
                    direction = "South"
                elif 203 <= wind_deg <= 247:
                    direction = "Southwest"
                elif 248 <= wind_deg <= 292:
                    direction = "West"
                elif 293 <= wind_deg <= 337:
                    direction = "Northwest"
                else:
                    direction = f"{wind_deg} degrees"
            
            wind_info = f"{direction} at {int(wind_speed)} knots{gust}"
            break
    
    # Extract visibility
    visibility = "Unknown"
    for i in range(start_index + 2, len(parts)):
        part = parts[i]
        # Handle visibility in meters
        if re.match(r'^\d{4}$', part) and int(part) < 9999:
            # Meters visibility
            meters = int(part)
            miles = meters / 1609.34
            visibility = f"{miles:.1f} miles"
            break
        # Handle fractional visibility in statute miles
        elif re.match(r'^\d/\d(?:SM)?$', part):
            if part.endswith("SM"):
                # Statute miles
                vis_value = part[:-2]
                visibility = f"{vis_value} statute miles"
            else:
                visibility = f"{part} statute miles"
            break
        # Handle whole number or mixed number visibility
        elif re.match(r'^\d+(?:\s\d/\d)?SM$', part):
            # Statute miles
            vis_value = part[:-2]
            visibility = f"{vis_value} statute miles"
            break
        elif part == "CAVOK":
            visibility = "Greater than 6 statute miles (Cloud and Visibility OK)"
            break
    
    # Extract weather conditions
    weather_conditions = []
    weather_codes = {
        '-': 'Light',
        '+': 'Heavy',
        'VC': 'In the vicinity',
        'MI': 'Shallow',
        'PR': 'Partial',
        'BC': 'Patches',
        'DR': 'Low drifting',
        'BL': 'Blowing',
        'SH': 'Showers',
        'TS': 'Thunderstorm',
        'FZ': 'Freezing',
        'DZ': 'Drizzle',
        'RA': 'Rain',
        'SN': 'Snow',
        'SG': 'Snow grains',
        'IC': 'Ice crystals',
        'PL': 'Ice pellets',
        'GR': 'Hail',
        'GS': 'Small hail',
        'UP': 'Unknown precipitation',
        'BR': 'Mist',
        'FG': 'Fog',
        'FU': 'Smoke',
        'VA': 'Volcanic ash',
        'DU': 'Dust',
        'SA': 'Sand',
        'HZ': 'Haze',
        'PY': 'Spray',
        'PO': 'Dust whirls',
        'SQ': 'Squalls',
        'FC': 'Funnel cloud/tornado',
        'SS': 'Sandstorm'
    }
    
    # Look for weather condition codes in the METAR
    for i in range(start_index + 2, len(parts)):
        part = parts[i]
        # Skip parts that are clearly not weather codes
        if re.match(r'^\d{3}\d{2}(?:G\d{2})?(?:KT|MPS|KMH)$', part) or \
           re.match(r'^\d{4}$', part) or \
           re.match(r'^\d+SM$', part) or \
           part.startswith('A') or part.startswith('Q') or \
           '/' in part:
            continue
            
        # Check if this part contains weather codes
        matched_conditions = []
        temp_part = part
        
        # Handle intensity modifiers
        if temp_part.startswith('-'):
            matched_conditions.append('Light')
            temp_part = temp_part[1:]
        elif temp_part.startswith('+'):
            matched_conditions.append('Heavy')
            temp_part = temp_part[1:]
        
        # Process weather codes
        while temp_part:
            found = False
            # Try to match longer codes first
            for length in [4, 3, 2]:
                if len(temp_part) >= length:
                    code = temp_part[:length]
                    if code in weather_codes:
                        matched_conditions.append(weather_codes[code])
                        temp_part = temp_part[length:]
                        found = True
                        break
            if not found and len(temp_part) >= 2:
                code = temp_part[:2]
                if code in weather_codes:
                    matched_conditions.append(weather_codes[code])
                    temp_part = temp_part[2:]
                    found = True
            if not found:
                # Skip unrecognized characters
                temp_part = temp_part[1:] if temp_part else ""
        
        if matched_conditions:
            weather_conditions.append(' '.join(matched_conditions))
    
    # Extract sky conditions
    sky_conditions = []
    sky_codes = {
        'SKC': 'Sky clear',
        'NCD': 'No clouds detected',
        'CLR': 'Clear',
        'NSC': 'No significant clouds',
        'FEW': 'Few clouds',
        'SCT': 'Scattered clouds',
        'BKN': 'Broken clouds',
        'VV': 'Vertical visibility',
        'OVC': 'Overcast'
    }
    
    for i in range(start_index + 2, len(parts)):
        part = parts[i]
        if 'CLR' in part:
            sky_conditions.append('Clear')
            break
        for code, description in sky_codes.items():
            if part.startswith(code):
                if code in ['FEW', 'SCT', 'BKN', 'OVC'] and len(part) > 3:
                    # Extract altitude information
                    altitude = part[3:]
                    if altitude.isdigit():
                        feet = int(altitude) * 100
                        sky_conditions.append(f"{description} at {feet} feet")
                    else:
                        sky_conditions.append(description)
                elif code in ['VV'] and len(part) > 2:
                    # Extract vertical visibility
                    vv = part[2:]
                    if vv.isdigit():
                        feet = int(vv) * 100
                        sky_conditions.append(f"Vertical visibility {feet} feet")
                    else:
                        sky_conditions.append(description)
                else:
                    sky_conditions.append(description)
                break
    
    # Extract temperature/dewpoint
    temp_dewpoint = "Unknown"
    for i in range(start_index + 2, len(parts)):
        part = parts[i]
        if '/' in part and len(part) >= 3 and len(part) <= 7:
            # Check if it looks like temperature/dewpoint
            if 'M' in part or part.replace('/', '').replace('M', '').isdigit():
                # Handle potential temperature/dewpoint
                if '/' in part:
                    temp_part, dew_part = part.split('/')
                    try:
                        # Handle negative temperatures (M prefix)
                        temp = int(temp_part.replace('M', '-')) if temp_part else 0
                        dew = int(dew_part.replace('M', '-')) if dew_part else 0
                        temp_dewpoint = f"Temperature {temp}°C, Dewpoint {dew}°C"
                        break
                    except:
                        continue
    
    # Extract altimeter (pressure)
    altimeter = "Unknown"
    for i in range(start_index + 2, len(parts)):
        part = parts[i]
        if part.startswith('A') and len(part) == 5 and part[1:].isdigit():
            # Inches of mercury
            alt_value = int(part[1:]) / 100
            altimeter = f"Altimeter {alt_value:.2f} inches of mercury"
            break
        elif part.startswith('Q') and len(part) == 5 and part[1:].isdigit():
            # Hectopascals
            alt_value = int(part[1:])
            altimeter = f"Altimeter {alt_value} hectopascals"
            break
    
    # Create friendly readable report
    report_lines = []
    report_lines.append(f"Weather report for {station_id}")
    report_lines.append(f"Day {day} at {time[:2]}:{time[2:]} UTC")
    
    # Wind information
    report_lines.append(f"Wind: {wind_info}")
        
    # Visibility
    if visibility != "Unknown":
        report_lines.append(f"Visibility: {visibility}")
        
    # Weather conditions
    if weather_conditions:
        report_lines.append(f"Weather: {', '.join(weather_conditions)}")
    elif sky_conditions:
        report_lines.append(f"Sky: {', '.join(sky_conditions)}")
    else:
        report_lines.append("Sky: Clear")
        
    # Temperature/Dewpoint
    if temp_dewpoint != "Unknown":
        report_lines.append(temp_dewpoint)
        
    # Altimeter
    if altimeter != "Unknown":
        report_lines.append(altimeter)
        
    return "\n".join(report_lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/metar', methods=['POST'])
def get_metar():
    station_id = request.form.get('station_id', '').upper()
    
    if not station_id:
        return jsonify({'error': 'Please enter a station ID'}), 400
    
    # Fetch METAR data
    metar_data = fetch_metar(station_id)
    
    if not metar_data:
        return jsonify({'error': f'Unable to fetch METAR data for {station_id}'}), 404
    
    # Decode METAR data
    decoded_report = decode_metar(metar_data)
    
    return jsonify({
        'station_id': station_id,
        'raw_metar': metar_data,
        'decoded_report': decoded_report
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)