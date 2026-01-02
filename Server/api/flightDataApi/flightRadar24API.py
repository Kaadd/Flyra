import os
from typing import Optional, Any, List

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, will use environment variables only

from .flight_data_interface import FlightDataInterface, FlightData


class FlightRadar24API(FlightDataInterface):
    """
    FlightRadar24 API implementation for fetching flight data.
    
    This class implements the FlightDataInterface to provide flight tracking
    data from FlightRadar24's API service.
    
    Note: 
    - This implementation uses the FlightRadar24 Live API to get REAL-TIME position data
      including altitude, speed, latitude, longitude, and direction.
    - Accepts flight numbers/callsigns (e.g., "UA837", "AA100") or FlightRadar24 flight_ids.
    - Returns LIVE tracking data for currently active flights.
    """
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the FlightRadar24 API client.
        
        Args:
            api_token: Optional API token. If not provided, will attempt to load
                      from environment variable FR24_API_TOKEN or FLIGHTRADARAPI_KEY.
        
        Raises:
            ValueError: If API token is not provided and not found in environment.
            ImportError: If fr24sdk library is not installed.
        """
        try:
            from fr24sdk.client import Client
        except ImportError:
            raise ImportError(
                "fr24sdk library is not installed. "
                "Install it with: pip install fr24sdk"
            )
        
        # Get API token from parameter or environment variable
        # fr24sdk uses FR24_API_TOKEN, but we also support FLIGHTRADARAPI_KEY for compatibility
        if api_token is None:
            api_token = os.getenv("FR24_API_TOKEN") or os.getenv("FLIGHTRADARAPI_KEY")
        
        # Note: fr24sdk Client will handle missing token and raise NoApiKeyError
        # We'll let it handle that rather than checking here, as the SDK may have
        # other ways to authenticate
        
        self.client = Client(api_token=api_token)

    def get_flight_data(self, flight_id: str) -> FlightData:
        """
        Fetch LIVE flight data for a given flight ID.
        
        Uses the FlightRadar24 Live API to get real-time position data including
        altitude, speed, latitude, longitude, and direction.
        
        Args:
            flight_id: Flight identifier. Can be:
                     - Flight number/callsign (e.g., "UA837", "AA100")
                     - FlightRadar24 flight_id (e.g., "abc123def456")
        
        Returns:
            FlightData object containing LIVE flight information with real-time position data
        
        Raises:
            ValueError: If flight_id is empty or invalid, or flight not found
            ConnectionError: If API request fails
            KeyError: If required flight data fields are missing
        """
        if not flight_id or not flight_id.strip():
            raise ValueError("flight_id cannot be empty")
        
        flight_id = flight_id.strip().upper()
        
        try:
            # Use LIVE API to get real-time position data
            # Try by flight number/callsign first (most common use case)
            response = self.client.live.flight_positions.get_full(flights=[flight_id])
            
            # Check if we got any data
            if not response or not response.data or len(response.data) == 0:
                # Try searching by FlightRadar24 flight_id if flight number didn't work
                response = self.client.live.flight_positions.get_full(
                    callsigns=[flight_id]
                )
                
                if not response or not response.data or len(response.data) == 0:
                    raise ValueError(
                        f"Flight {flight_id} not found in live tracking data. "
                        "The flight may not be currently active or the flight ID may be incorrect."
                    )
            
            # Get the first flight from the response (most recent/active)
            flight = response.data[0]
            
        except ValueError:
            # Re-raise ValueError as-is
            raise
        except Exception as e:
            # Handle API errors
            from fr24sdk.exceptions import NoApiKeyError, NotFoundError, ApiError
            
            if isinstance(e, NoApiKeyError):
                raise ValueError(
                    "FlightRadar24 API token is required. "
                    "Set FR24_API_TOKEN environment variable or pass api_token parameter."
                ) from e
            elif isinstance(e, NotFoundError):
                raise ValueError(f"Flight {flight_id} not found") from e
            elif isinstance(e, ApiError):
                raise ConnectionError(
                    f"FlightRadar24 API error for {flight_id}: {str(e)}"
                ) from e
            else:
                raise ConnectionError(
                    f"Failed to fetch live flight data for {flight_id}: {str(e)}"
                ) from e
        
        # Extract LIVE flight data from the response
        # FlightPositionsFull contains real-time position data
        try:
            # Get airport codes (prefer IATA, fallback to ICAO)
            departure_airport = (
                self._safe_str(flight.orig_iata) 
                if flight.orig_iata 
                else self._safe_str(flight.orig_icao)
            )
            arrival_airport = (
                self._safe_str(flight.dest_iata)
                if flight.dest_iata
                else self._safe_str(flight.dest_icao)
            )
            
            # Extract LIVE position data
            return FlightData(
                flight_id=self._safe_str(flight.fr24_id),
                flight_altitude=self._safe_int(flight.alt),  # Altitude in feet
                flight_speed=self._safe_int(flight.gspeed),  # Ground speed (knots)
                flight_latitude=self._safe_float(flight.lat),  # Latitude
                flight_longitude=self._safe_float(flight.lon),  # Longitude
                flight_direction=self._safe_int(flight.track),  # Track/direction in degrees
                flight_departure_airport=departure_airport,
                flight_arrival_airport=arrival_airport
            )
        except (AttributeError, TypeError) as e:
            raise KeyError(
                f"Missing required flight data fields for {flight_id}: {str(e)}"
            ) from e
    
    @staticmethod
    def _safe_int(value: Optional[Any]) -> int:
        """Safely convert value to int, defaulting to 0 if None or invalid."""
        if value is None:
            return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0
    
    @staticmethod
    def _safe_float(value: Optional[Any]) -> float:
        """Safely convert value to float, defaulting to 0.0 if None or invalid."""
        if value is None:
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def _safe_str(value: Optional[Any]) -> str:
        """Safely convert value to string, defaulting to 'Unknown' if None."""
        if value is None:
            return "Unknown"
        return str(value)
