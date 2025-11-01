from typing import Any, Optional

def format_distance(distance_km: float) -> str:
    """Format distance for display"""
    if distance_km < 1:
        return f"{distance_km * 1000:.0f}m"
    return f"{distance_km:.2f}km"

def format_pace(pace_min_per_km: float) -> str:
    """Format pace as MM:SS per km"""
    minutes = int(pace_min_per_km)
    seconds = int((pace_min_per_km - minutes) * 60)
    return f"{minutes}:{seconds:02d}"

def format_duration(seconds: int) -> str:
    """Format duration as HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"
