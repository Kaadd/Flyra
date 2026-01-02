"""
Flight Data API package.

This package provides interfaces and implementations for fetching
flight tracking data from various sources.
"""

from .flight_data_interface import FlightDataInterface, FlightData
from .flightRadar24API import FlightRadar24API

__all__ = [
    "FlightDataInterface",
    "FlightData",
    "FlightRadar24API",
]

