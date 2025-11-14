"""
GPS Parser Module

This module provides utilities for extracting GPS coordinates from image metadata
and handling geographic data in the RhinoGuardians system.
"""

from typing import Optional, Tuple
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_gps_from_image(image_path: str) -> Optional[Tuple[float, float]]:
    """
    Extract GPS coordinates from image EXIF data.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        Optional[Tuple[float, float]]: Tuple of (latitude, longitude) if found,
                                     None if no GPS data exists
    """
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
            if not exif:
                return None
                
            gps_info = None
            for tag_id in exif:
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    gps_info = exif[tag_id]
                    break
                    
            if not gps_info:
                return None
                
            lat_data = gps_info.get(2)  # Latitude data
            lon_data = gps_info.get(4)  # Longitude data
            lat_ref = gps_info.get(1, 'N')  # North/South
            lon_ref = gps_info.get(3, 'E')  # East/West
            
            if not (lat_data and lon_data):
                return None
                
            # Convert coordinates to degrees
            lat = _convert_to_degrees(lat_data)
            lon = _convert_to_degrees(lon_data)
            
            # Apply hemisphere reference
            if lat_ref == 'S':
                lat = -lat
            if lon_ref == 'W':
                lon = -lon
                
            return (lat, lon)
            
    except Exception as e:
        print(f"Error extracting GPS data: {e}")
        return None

def _convert_to_degrees(value: tuple) -> float:
    """
    Helper function to convert GPS coordinates to decimal degrees.
    
    Args:
        value (tuple): GPS coordinate tuple (degrees, minutes, seconds)
        
    Returns:
        float: Decimal degrees
    """
    degrees = value[0]
    minutes = value[1]
    seconds = value[2]
    
    return degrees + (minutes / 60.0) + (seconds / 3600.0)