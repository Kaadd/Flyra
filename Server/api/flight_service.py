import os
import httpx
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AVIATION_STACK_BASE_URL = "https://api.aviationstack.com/v1"
API_KEY = os.getenv("API_KEY")


async def get_flight_info(flight_number: str) -> Optional[Dict[str, Any]]:
    """
    Fetch flight information from Aviation Stack API.
    
    Args:
        flight_number: Flight number (e.g., "UA837", "AA100")
    
    Returns:
        Dictionary with flight information or None if not found
    """
    if not API_KEY:
        raise ValueError("API_KEY not found in environment variables")
    
    # Clean flight number (remove spaces, convert to uppercase)
    flight_number = flight_number.strip().upper()
    
    # Extract airline code and flight number if needed
    # Aviation Stack expects format like "UA837" or separate iata code
    params = {
        "access_key": API_KEY,
        "flight_iata": flight_number,
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{AVIATION_STACK_BASE_URL}/flights",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            # Check if we have flight data
            if data.get("data") and len(data["data"]) > 0:
                flight_data = data["data"][0]
                return format_flight_response(flight_data, flight_number)
            else:
                return None
                
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid API key")
        elif e.response.status_code == 429:
            raise ValueError("API rate limit exceeded")
        else:
            raise ValueError(f"API error: {e.response.status_code}")
    except httpx.RequestError as e:
        raise ValueError(f"Network error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error fetching flight data: {str(e)}")


def format_flight_response(flight_data: Dict[str, Any], flight_number: str) -> Dict[str, Any]:
    """
    Format Aviation Stack API response to match our frontend format.
    
    Args:
        flight_data: Raw flight data from Aviation Stack API
        flight_number: Original flight number query
    
    Returns:
        Formatted flight data dictionary
    """
    flight_info = flight_data.get("flight", {})
    departure = flight_data.get("departure", {})
    arrival = flight_data.get("arrival", {})
    airline = flight_info.get("iata", "")
    aircraft = flight_data.get("aircraft", {})
    
    # Extract flight status
    flight_status = flight_data.get("flight_status", "unknown").title()
    
    # Format departure time
    departure_time = departure.get("scheduled", "")
    if departure_time:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(departure_time.replace("Z", "+00:00"))
            flight_time = dt.strftime("%I:%M %p")
        except:
            flight_time = departure_time
    else:
        flight_time = "TBD"
    
    # Format date
    departure_date = departure.get("scheduled", "")
    if departure_date:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(departure_date.replace("Z", "+00:00"))
            flight_date = dt.strftime("%Y-%m-%d")
        except:
            flight_date = departure_date.split("T")[0] if "T" in departure_date else departure_date
    else:
        flight_date = "TBD"
    
    # Get gate and terminal
    gate = departure.get("gate", "TBD")
    terminal = departure.get("terminal", "TBD")
    
    # Get additional flight details for AI context
    aircraft_type = aircraft.get("iata", "") or aircraft.get("icao24", "") or "Unknown"
    departure_airport = departure.get("airport", "") or departure.get("iata", "")
    arrival_airport = arrival.get("airport", "") or arrival.get("iata", "")
    departure_delay = departure.get("delay")
    arrival_delay = arrival.get("delay")
    
    return {
        "flight_id": flight_number,
        "flight_number": flight_info.get("number", flight_number),
        "flight_status": flight_status,
        "flight_time": flight_time,
        "flight_date": flight_date,
        "flight_gate": gate if gate else "TBD",
        "flight_terminal": terminal if terminal else "TBD",
        # Additional context for AI
        "aircraft_type": aircraft_type,
        "departure_airport": departure_airport,
        "arrival_airport": arrival_airport,
        "departure_delay": departure_delay,
        "arrival_delay": arrival_delay,
        "raw_data": flight_data  # Include raw data for more context
    }

