# METAR Reader

A Flask web application that decodes METAR (Meteorological Terminal Aviation Routine Weather Report) into plain English.

## What is METAR?

METAR is a standardized format for reporting weather information at airports. These reports are used by pilots, air traffic controllers, and meteorologists but can be difficult for the general public to understand. This application translates these cryptic codes into simple, readable weather reports.

## Features

- Enter any 4-letter ICAO airport code
- Fetches real-time METAR data from aviationweather.gov
- Decodes METAR into plain English:
  - Wind direction and speed
  - Visibility
  - Weather conditions
  - Sky conditions
  - Temperature and dewpoint
  - Atmospheric pressure

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000`

3. Enter a 4-letter ICAO airport code (e.g., KHIO for Hillsboro Airport)

4. View the decoded weather report in plain English

## Example Airport Codes

- KHIO - Hillsboro Airport, Oregon
- KJFK - John F. Kennedy International Airport, New York
- KLAX - Los Angeles International Airport
- KORD - Chicago O'Hare International Airport
- KSFO - San Francisco International Airport

## How It Works

1. The application sends a request to `https://aviationweather.gov/api/data/metar?ids={STATION_ID}`
2. The METAR data is parsed and decoded using regular expressions
3. The cryptic codes are translated into plain English descriptions
4. The results are displayed in a user-friendly web interface

## Technologies Used

- Python
- Flask (web framework)
- HTML/CSS/JavaScript (frontend)
- Requests (for API calls)