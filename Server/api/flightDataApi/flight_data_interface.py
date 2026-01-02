from abc import ABC, abstractmethod
from typing import Optional


class FlightData:
    """
    Data class representing flight tracking information.
    
    Attributes:
        flight_id: Unique flight identifier (e.g., "UA837")
        flight_altitude: Current altitude in feet
        flight_speed: Current speed (units depend on API, typically mph or knots)
        flight_latitude: Current latitude coordinate
        flight_longitude: Current longitude coordinate
        flight_direction: Current heading/direction in degrees (0-360)
        flight_departure_airport: Departure airport code or name
        flight_arrival_airport: Arrival airport code or name
    """
    
    def __init__(
        self,
        flight_id: str,
        flight_altitude: int,
        flight_speed: int,
        flight_latitude: float,
        flight_longitude: float,
        flight_direction: int,
        flight_departure_airport: str,
        flight_arrival_airport: str
    ):
        """
        Initialize FlightData with flight tracking information.
        
        Args:
            flight_id: Unique flight identifier
            flight_altitude: Altitude in feet
            flight_speed: Speed (units depend on API)
            flight_latitude: Latitude coordinate
            flight_longitude: Longitude coordinate
            flight_direction: Heading in degrees (0-360)
            flight_departure_airport: Departure airport identifier
            flight_arrival_airport: Arrival airport identifier
        """
        self.flight_id = flight_id
        self.flight_altitude = flight_altitude
        self.flight_speed = flight_speed
        self.flight_latitude = flight_latitude
        self.flight_longitude = flight_longitude
        self.flight_direction = flight_direction
        self.flight_departure_airport = flight_departure_airport
        self.flight_arrival_airport = flight_arrival_airport
    
    def to_dict(self) -> dict:
        """
        Convert FlightData to dictionary format.
        
        Returns:
            Dictionary representation of flight data
        """
        return {
            "flight_id": self.flight_id,
            "flight_altitude": self.flight_altitude,
            "flight_speed": self.flight_speed,
            "flight_latitude": self.flight_latitude,
            "flight_longitude": self.flight_longitude,
            "flight_direction": self.flight_direction,
            "flight_departure_airport": self.flight_departure_airport,
            "flight_arrival_airport": self.flight_arrival_airport,
        }
    
    def __repr__(self) -> str:
        """String representation of FlightData."""
        return (
            f"FlightData(flight_id='{self.flight_id}', "
            f"altitude={self.flight_altitude}ft, "
            f"speed={self.flight_speed}, "
            f"position=({self.flight_latitude}, {self.flight_longitude}))"
        )


class FlightDataInterface(ABC):
    """
    Abstract interface for flight data providers.
    
    This interface defines the contract that all flight data API
    implementations must follow, allowing for easy swapping of
    different flight data sources.
    """
    
    @abstractmethod
    def get_flight_data(self, flight_id: str) -> FlightData:
        """
        Fetch flight data for a given flight ID.
        
        Args:
            flight_id: Flight identifier (e.g., "UA837", "AA100")
        
        Returns:
            FlightData object containing flight information
        
        Raises:
            ValueError: If flight_id is invalid or flight not found
            ConnectionError: If API request fails
        """
        pass