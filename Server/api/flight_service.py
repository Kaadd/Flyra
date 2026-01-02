"""
Flight service module for Flyra API.

This module provides live flight data using the FlightRadar24 API.
No mock data - all data is real-time from FlightRadar24.
"""

from typing import Optional, Dict, Any
from datetime import datetime

from .flightDataApi import FlightRadar24API, FlightData


# Singleton instance of the FlightRadar24 API client
_flight_api: Optional[FlightRadar24API] = None


def get_flight_api() -> FlightRadar24API:
    """
    Get the singleton FlightRadar24 API client instance.
    
    Returns:
        FlightRadar24API: The API client instance
    """
    global _flight_api
    if _flight_api is None:
        _flight_api = FlightRadar24API()
    return _flight_api


def _knots_to_mph(knots: int) -> int:
    """Convert knots to miles per hour."""
    return int(knots * 1.15078)


async def get_flight_info(flight_number: str) -> Optional[Dict[str, Any]]:
    """
    Get LIVE flight information from FlightRadar24 API.
    
    This function fetches real-time flight data including position,
    altitude, speed, and route information.
    
    Args:
        flight_number: Flight number/callsign (e.g., "UA837", "AA100")
    
    Returns:
        Dictionary with live flight information or None if not found
        Compatible with the Swift Flight model
    
    Raises:
        ValueError: If API token is missing or flight number is invalid
        ConnectionError: If API request fails
    """
    if not flight_number or not flight_number.strip():
        return None
    
    flight_number = flight_number.strip().upper()
    
    try:
        api = get_flight_api()
        flight_data: FlightData = api.get_flight_data(flight_number)
        
        # Get current timestamp for the response
        now = datetime.now()
        
        # Convert speed from knots to mph for Swift app compatibility
        speed_mph = _knots_to_mph(flight_data.flight_speed)
        
        # Build the response dictionary with live data
        # All fields match the Swift Flight model CodingKeys
        return {
            # Required fields for Swift Flight model
            "flight_id": flight_data.flight_id,
            "flight_number": flight_number,
            "flight_status": "In Flight",
            "flight_time": now.strftime("%I:%M %p"),
            "flight_date": now.strftime("%Y-%m-%d"),
            "flight_gate": "N/A",  # Not available from FlightRadar24
            "flight_terminal": "N/A",  # Not available from FlightRadar24
            
            # Optional fields
            "aircraft_type": None,  # Not available in live API
            "departure_airport": flight_data.flight_departure_airport,
            "arrival_airport": flight_data.flight_arrival_airport,
            "departure_delay": None,
            "arrival_delay": None,
            
            # LIVE tracking data (real-time from FlightRadar24)
            "altitude_ft": flight_data.flight_altitude,
            "speed_mph": speed_mph,  # Converted from knots for Swift compatibility
            "speed_knots": flight_data.flight_speed,  # Original value in knots
            "latitude": flight_data.flight_latitude,
            "longitude": flight_data.flight_longitude,
            "direction": flight_data.flight_direction,
            
            # Airport coordinates (not available in live API)
            "departure_latitude": None,
            "departure_longitude": None,
            "arrival_latitude": None,
            "arrival_longitude": None,
            
            # ETA and distance (not available in live API)
            "eta": None,
            "distance_miles": None,
            
            # Metadata
            "last_updated": now.isoformat(),
            "data_source": "flightradar24",
            "is_live": True,
        }
        
    except ValueError as e:
        # Flight not found or invalid input
        error_msg = str(e)
        if "not found" in error_msg.lower():
            return None
        raise
    except ConnectionError:
        # API connection error - re-raise
        raise
    except Exception as e:
        # Unexpected error
        raise ConnectionError(f"Failed to fetch flight data: {str(e)}") from e


async def search_flights_by_route(
    departure: Optional[str] = None,
    arrival: Optional[str] = None,
    limit: int = 10
) -> list[Dict[str, Any]]:
    """
    Search for live flights by route (departure/arrival airports).
    
    Args:
        departure: Departure airport IATA code (e.g., "JFK")
        arrival: Arrival airport IATA code (e.g., "LAX")
        limit: Maximum number of results to return
    
    Returns:
        List of flight dictionaries compatible with Swift Flight model
    """
    if not departure and not arrival:
        return []
    
    try:
        api = get_flight_api()
        
        # Build route query
        routes = []
        if departure and arrival:
            routes = [f"{departure.upper()}-{arrival.upper()}"]
        elif departure:
            routes = [f"{departure.upper()}-"]
        elif arrival:
            routes = [f"-{arrival.upper()}"]
        
        # Query the live API
        response = api.client.live.flight_positions.get_full(
            routes=routes,
            limit=limit
        )
        
        if not response or not response.data:
            return []
        
        # Convert to response format compatible with Swift Flight model
        now = datetime.now()
        flights = []
        
        for flight in response.data:
            speed_knots = flight.gspeed
            speed_mph = _knots_to_mph(speed_knots)
            flight_number = flight.flight or flight.callsign or "Unknown"
            
            flights.append({
                # Required fields
                "flight_id": flight.fr24_id,
                "flight_number": flight_number,
                "flight_status": "In Flight",
                "flight_time": now.strftime("%I:%M %p"),
                "flight_date": now.strftime("%Y-%m-%d"),
                "flight_gate": "N/A",
                "flight_terminal": "N/A",
                
                # Optional fields
                "departure_airport": flight.orig_iata or flight.orig_icao or "Unknown",
                "arrival_airport": flight.dest_iata or flight.dest_icao or "Unknown",
                "altitude_ft": flight.alt,
                "speed_mph": speed_mph,
                "speed_knots": speed_knots,
                "latitude": flight.lat,
                "longitude": flight.lon,
                "direction": flight.track,
                
                # Metadata
                "last_updated": now.isoformat(),
                "data_source": "flightradar24",
                "is_live": True,
            })
        
        return flights
        
    except Exception as e:
        raise ConnectionError(f"Failed to search flights: {str(e)}") from e
