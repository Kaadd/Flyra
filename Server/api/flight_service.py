import random
import math
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from .airport_coordinates import get_airport_coordinates, AIRPORT_COORDINATES

# Allowed flight numbers and their routes
FLIGHT_ROUTES = {
    "AB61510": {"dep": "SFO", "arr": "NRT", "dep_name": "San Francisco International", "arr_name": "Narita International Airport"},
    "ZZ001": {"dep": "JFK", "arr": "LHR", "dep_name": "John F. Kennedy International", "arr_name": "London Heathrow"},
}

# List of allowed flight numbers
ALLOWED_FLIGHT_NUMBERS = {"AB61510", "ZZ001"}


async def get_flight_info(flight_number: str) -> Optional[Dict[str, Any]]:
    """
    Generate fake flight information.
    
    Args:
        flight_number: Flight number (must be "AB61510" or "ZZ001")
    
    Returns:
        Dictionary with flight information or None if not found
    """
    # Clean flight number (remove spaces, convert to uppercase)
    flight_number = flight_number.strip().upper()
    
    # Only allow specific flight numbers
    if flight_number not in ALLOWED_FLIGHT_NUMBERS:
        return None
    
    # Get route info (should always exist since we validated above)
    route = FLIGHT_ROUTES.get(flight_number)
    if not route:
        return None
    
    # Get airport coordinates
    dep_coords = get_airport_coordinates(route["dep"])
    arr_coords = get_airport_coordinates(route["arr"])
    
    # Generate fake live tracking data
    # Calculate a point along the route (about 60% of the way)
    if dep_coords and arr_coords:
        dep_lat, dep_lng = dep_coords
        arr_lat, arr_lng = arr_coords
        
        # Interpolate position (60% along route)
        progress = 0.6
        current_lat = dep_lat + (arr_lat - dep_lat) * progress
        current_lng = dep_lng + (arr_lng - dep_lng) * progress
        
        # Calculate direction (bearing)
        lat1, lon1 = math.radians(dep_lat), math.radians(dep_lng)
        lat2, lon2 = math.radians(arr_lat), math.radians(arr_lng)
        dlon = lon2 - lon1
        y = math.sin(dlon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        direction = int((math.degrees(math.atan2(y, x)) + 360) % 360)
        
        # Calculate distance remaining
        R = 3959  # Earth radius in miles
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        total_distance = R * c
        distance_miles = int(total_distance * (1 - progress))
    else:
        current_lat = 40.0
        current_lng = -100.0
        direction = 270
        distance_miles = 2500
    
    # Generate realistic flight data
    now = datetime.now()
    flight_time = now.strftime("%I:%M %p")
    flight_date = now.strftime("%Y-%m-%d")
    
    # Random but realistic values
    altitude_ft = random.randint(35000, 40000)  # Cruising altitude
    speed_mph = random.randint(500, 600)  # Typical cruising speed
    
    # Calculate ETA (about 2-3 hours from now for long flights)
    eta_time = now + timedelta(hours=random.randint(2, 3))
    eta = eta_time.strftime("%I:%M %p")
    
    # Flight status
    statuses = ["Active", "On time", "In flight", "En route"]
    flight_status = random.choice(statuses)
    
    return {
        "flight_id": flight_number,
        "flight_number": flight_number,
        "flight_status": flight_status,
        "flight_time": flight_time,
        "flight_date": flight_date,
        "flight_gate": f"G{random.randint(1, 20)}",
        "flight_terminal": str(random.randint(1, 5)),
        # Additional context
        "aircraft_type": "Boeing 777",
        "departure_airport": route["dep_name"],
        "arrival_airport": route["arr_name"],
        "departure_delay": None,
        "arrival_delay": None,
        # Live tracking data
        "altitude_ft": altitude_ft,
        "speed_mph": speed_mph,
        "latitude": current_lat,
        "longitude": current_lng,
        "direction": direction,
        # Airport coordinates
        "departure_latitude": dep_coords[0] if dep_coords else None,
        "departure_longitude": dep_coords[1] if dep_coords else None,
        "arrival_latitude": arr_coords[0] if arr_coords else None,
        "arrival_longitude": arr_coords[1] if arr_coords else None,
        # ETA and distance
        "eta": eta,
        "distance_miles": distance_miles,
        "raw_data": {}  # Empty for fake data
    }



