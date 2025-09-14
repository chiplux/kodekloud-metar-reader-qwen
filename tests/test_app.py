import pytest
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import decode_metar, fetch_metar

def test_decode_metar_basic():
    """Test basic METAR decoding functionality"""
    # Test a simple METAR string
    metar_text = "METAR KHIO 141253Z 18005KT 10SM CLR 16/15 A2987"
    result = decode_metar(metar_text)
    
    assert "Weather report for KHIO" in result
    assert "Day 14 at 12:53 UTC" in result
    assert "Wind: South at 5 knots" in result
    assert "Visibility: 10 statute miles" in result
    assert "Sky: Clear" in result
    assert "Temperature 16°C, Dewpoint 15°C" in result
    assert "Altimeter 29.87 inches of mercury" in result

def test_decode_metar_with_weather():
    """Test METAR decoding with weather conditions"""
    # Test METAR with weather conditions
    metar_text = "SPECI KHIO 141311Z 17004KT 10SM -RA SCT012 BKN022 OVC095 16/15 A2987"
    result = decode_metar(metar_text)
    
    assert "Weather report for KHIO" in result
    assert "Day 14 at 13:11 UTC" in result
    assert "Wind: South at 4 knots" in result
    assert "Visibility: 10 statute miles" in result
    assert "Weather: Light Rain" in result

def test_decode_metar_with_gusts():
    """Test METAR decoding with wind gusts"""
    # Test METAR with wind gusts
    metar_text = "METAR KLAX 141253Z 23006G12KT 10SM CLR 20/17 A2987"
    result = decode_metar(metar_text)
    
    assert "Weather report for KLAX" in result
    assert "Wind: Southwest at 6 knots gusting to 12 knots" in result

def test_fetch_metar_returns_string_or_none():
    """Test that fetch_metar returns a string or None"""
    # Test with a valid station ID
    result = fetch_metar("KHIO")
    assert isinstance(result, str) or result is None
    
    # Test with an invalid station ID
    result = fetch_metar("INVALID")
    assert result is None or isinstance(result, str)