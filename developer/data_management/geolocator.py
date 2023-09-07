"""Function(s) for geolocation"""
import pandas as pd
import numpy as np

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="myGeocoder")

def _get_state_from_coordinates(latitude, longitude, attempt=1, max_attempts=5):
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.raw['address']
        state = address.get('state', '')
        return state
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return _get_state_from_coordinates(latitude, longitude, attempt=attempt+1)
        raise

def classify_state(row):
    latitude = row['LocationLatitude']
    longitude = row['LocationLongitude']
    state = _get_state_from_coordinates(latitude, longitude)
    return state