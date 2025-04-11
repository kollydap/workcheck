# app/utils/geolocation.py
import math
from typing import Tuple, Optional


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance in meters between two coordinates
    using the Haversine formula
    """
    # Earth radius in meters
    R = 6371000

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


def is_within_radius(
    user_lat: float,
    user_lon: float,
    target_lat: float,
    target_lon: float,
    radius_meters: float = 100,
) -> bool:
    """
    Check if user coordinates are within specified radius of target coordinates
    """
    distance = calculate_distance(user_lat, user_lon, target_lat, target_lon)
    return distance <= radius_meters
