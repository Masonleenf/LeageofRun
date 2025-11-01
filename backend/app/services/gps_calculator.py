from math import radians, cos, sin, asin, sqrt
from typing import List, Tuple

class GPSCalculator:
    """GPS distance and statistics calculator"""

    EARTH_RADIUS_KM = 6371

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS points using Haversine formula
        Returns distance in kilometers
        """
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))

        distance_km = GPSCalculator.EARTH_RADIUS_KM * c
        return distance_km

    @staticmethod
    def calculate_total_distance(route: List[Tuple[float, float]]) -> float:
        """Calculate total distance from list of (lat, lng) coordinates"""
        if len(route) < 2:
            return 0.0

        total_distance = 0.0
        for i in range(len(route) - 1):
            lat1, lon1 = route[i]
            lat2, lon2 = route[i + 1]
            segment_distance = GPSCalculator.haversine_distance(lat1, lon1, lat2, lon2)
            total_distance += segment_distance

        return total_distance

    @staticmethod
    def calculate_pace(distance_km: float, duration_seconds: int) -> float:
        """Calculate pace in minutes per kilometer"""
        if distance_km <= 0:
            return 0.0
        duration_minutes = duration_seconds / 60
        pace = duration_minutes / distance_km
        return round(pace, 2)

    @staticmethod
    def calculate_speed(distance_km: float, duration_seconds: int) -> float:
        """Calculate speed in kilometers per hour"""
        if duration_seconds <= 0:
            return 0.0
        duration_hours = duration_seconds / 3600
        speed = distance_km / duration_hours
        return round(speed, 2)

    @staticmethod
    def calculate_calories(distance_km: float, weight_kg: float = 70, running: bool = True) -> float:
        """Calculate calories burned"""
        if running:
            calories = weight_kg * distance_km * 1.0
        else:
            calories = weight_kg * distance_km * 0.5
        return round(calories, 2)
