# METAR Reader

A Flask web application that decodes METAR (Meteorological Terminal Aviation Routine Weather Report) into plain English.

## What is METAR?

METAR is a standardized format for reporting weather information at airports. These reports are used by pilots, air traffic controllers, and meteorologists but can be difficult for the general public to understand. This application translates these cryptic codes into simple, readable weather reports.

## Features

- Enter any 4-letter ICAO airport code
- Fetches real-time METAR data from aviationweather.gov
- Decodes METAR into plain English:
  - Wind direction and speed (converted to compass directions)
  - Visibility conditions
  - Weather phenomena (rain, fog, snow, etc.)
  - Sky conditions and cloud cover
  - Temperature and dewpoint
  - Atmospheric pressure (altimeter)
- Responsive web interface that works on desktop and mobile devices
- Example airport codes for quick testing
- Real-time weather data

## Installation

### Option 1: Using Docker (Recommended)

1. Clone or download this repository:
   ```
   git clone <repository-url>
   cd kodekloud-metar-reader
   ```

2. Build and run the Docker container:
   ```
   make deploy
   ```

3. Access the application at `http://localhost:5000`

### Option 2: Manual Installation

1. Clone or download this repository:
   ```
   git clone <repository-url>
   cd kodekloud-metar-reader
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

5. Run the Flask application:
   ```
   python app.py
   ```

6. Open your web browser and go to `http://localhost:5000`

## Usage

1. Enter a 4-letter ICAO airport code (e.g., KHIO for Hillsboro Airport)
2. View the decoded weather report in plain English

## Example Airport Codes

- KHIO - Hillsboro Airport, Oregon
- KJFK - John F. Kennedy International Airport, New York
- KLAX - Los Angeles International Airport
- KORD - Chicago O'Hare International Airport
- KSFO - San Francisco International Airport
- KDEN - Denver International Airport
- KSEA - Seattle-Tacoma International Airport
- KMIA - Miami International Airport

## Docker Commands

The application includes a Makefile with convenient commands:

```
make build      # Build the Docker image (production)
make build-dev  # Build the Docker image (development)
make run        # Run the application in a container (production)
make run-dev    # Run the application in a container (development)
make dev        # Run the application in development mode with live reload
make stop       # Stop the running container
make test       # Run unit tests
make test-dev   # Run unit tests in development container
make clean      # Remove the Docker images
make logs       # View container logs
make shell      # Access the container shell
make shell-dev  # Access the development container shell
make deploy     # Build and deploy the application
make size       # Show Docker image sizes
make help       # Show all available commands
```

## Docker Compose

You can also use Docker Compose for development:

```
docker-compose up -d    # Start the application
docker-compose down     # Stop the application
```

## Image Optimization

This application uses a multi-stage Docker build to minimize image size:

1. **Builder Stage**: Installs build dependencies and Python packages
2. **Runtime Stage**: Uses a minimal Alpine Linux base with only runtime dependencies
3. **Non-root User**: Runs the application as a non-root user for security
4. **Separate Requirements**: Production and development dependencies are separated

The production image is significantly smaller than a single-stage build, reducing:
- Attack surface
- Network transfer time
- Storage requirements
- Startup time

To check image sizes:
```
make size
```

## How It Works

1. The application sends a request to `https://aviationweather.gov/api/data/metar?ids={STATION_ID}`
2. The METAR data is parsed and decoded using regular expressions and custom logic
3. The cryptic codes are translated into plain English descriptions:
   - Wind direction (e.g., "18005KT" becomes "South at 5 knots")
   - Visibility (e.g., "10SM" becomes "10 statute miles")
   - Weather conditions (e.g., "-RA" becomes "Light Rain")
   - Sky conditions (e.g., "SCT009 BKN013" becomes "Scattered clouds at 900 feet, Broken clouds at 1300 feet")
   - Temperature/Dewpoint (e.g., "16/15" becomes "Temperature 16°C, Dewpoint 15°C")
   - Altimeter (e.g., "A2987" becomes "Altimeter 29.87 inches of mercury")
4. The results are displayed in a user-friendly web interface

## METAR Decoding Examples

### Sample METAR Report:
```
METAR KHIO 141253Z AUTO 18005KT 10SM -RA SCT009 BKN013 OVC090 16/15 A2987 RMK AO2 SLP111 P0001 T01610150
```

### Decoded Report:
```
Weather report for KHIO
Day 14 at 12:53 UTC
Wind: South at 5 knots
Visibility: 10 statute miles
Weather: Light Rain
Sky: Scattered clouds at 900 feet, Broken clouds at 1300 feet, Overcast at 9000 feet
Temperature 16°C, Dewpoint 15°C
Altimeter 29.87 inches of mercury
```

## Technologies Used

- Python 3.x
- Flask (web framework)
- HTML5/CSS3/JavaScript (frontend)
- Requests library (for API calls)
- Regular expressions (for parsing)
- Docker (containerization)
- Makefile (build automation)

## API Endpoints

- `GET /` - Serve the main web interface
- `POST /metar` - API endpoint to fetch and decode METAR data

## Testing

Run unit tests with:
```
make test-dev
```

Or directly with pytest:
```
python -m pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Aviation Weather API provided by [aviationweather.gov](https://aviationweather.gov)
- Thanks to the open-source community for the tools and libraries used in this project