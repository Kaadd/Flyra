"""
Flyra API - Flight anxiety relief application backend.

This API provides real-time flight tracking data from FlightRadar24
and AI-powered calming messages for anxious passengers.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from mangum import Mangum
from typing import Optional

from .flight_service import get_flight_info, search_flights_by_route
from .ai_service import simple_chat


# Initialize FastAPI app
app = FastAPI(
    title="Flyra API",
    version="2.0.0",
    description="Real-time flight tracking and calming assistant for anxious passengers"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health & Info Endpoints
# =============================================================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Flyra API",
        "version": "2.0.0",
        "status": "running",
        "data_source": "FlightRadar24 (live data)"
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# =============================================================================
# Flight Endpoints
# =============================================================================

@app.get("/api/flight", tags=["Flight"])
async def get_flight(
    flight_id: str = Query(..., description="Flight number or callsign (e.g., 'UA837', 'AA100')")
):
    """
    Get LIVE flight information from FlightRadar24 API.
    
    Returns real-time position, altitude, speed, and route information
    for the specified flight.
    
    Args:
        flight_id: Flight number or callsign
    
    Returns:
        Live flight data including position and route information
    """
    try:
        flight_data = await get_flight_info(flight_id)
        
        if flight_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Flight '{flight_id}' not found. The flight may not be currently active."
            )
        
        return flight_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Flight data service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/flights/search", tags=["Flight"])
async def search_flights(
    departure: Optional[str] = Query(None, description="Departure airport IATA code (e.g., 'JFK')"),
    arrival: Optional[str] = Query(None, description="Arrival airport IATA code (e.g., 'LAX')"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """
    Search for live flights by route.
    
    At least one of departure or arrival airport must be specified.
    
    Args:
        departure: Departure airport IATA code
        arrival: Arrival airport IATA code
        limit: Maximum number of results (1-100)
    
    Returns:
        List of live flights matching the route criteria
    """
    if not departure and not arrival:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'departure' or 'arrival' must be specified"
        )
    
    try:
        flights = await search_flights_by_route(
            departure=departure,
            arrival=arrival,
            limit=limit
        )
        
        return {
            "count": len(flights),
            "flights": flights
        }
        
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Flight data service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# =============================================================================
# AI Chat Endpoints
# =============================================================================

class ChatRequest(BaseModel):
    """Request model for AI chat endpoint."""
    message: str = Field(..., description="User message to send to the AI")
    system_prompt: Optional[str] = Field(None, description="Optional custom system prompt")


@app.post("/api/ai/chat", tags=["AI"])
async def ai_chat(request: ChatRequest):
    """
    AI chat endpoint for general conversations.
    
    Args:
        request: Chat request with message and optional system prompt
    
    Returns:
        AI-generated response
    """
    try:
        response = await simple_chat(
            user_message=request.message,
            system_prompt=request.system_prompt
        )
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


# =============================================================================
# Calming Message Endpoint
# =============================================================================

CALMING_SYSTEM_PROMPT = """You are a flight calming assistant. Your job is to reassure passengers that everything is fine and normal. Be very calming, reassuring, and emphasize that everything is operating normally.

IMPORTANT: 
- You MUST use the EXACT altitude and speed values provided (do not make up numbers)
- Always reassure that everything is fine and normal
- Keep it brief (1-2 sentences)
- Be very calming and reassuring

Examples based on flight phase:
- Taxiing: "The scrubbing noise you might've heard is coming from the PTU (Power Transfer Unit), which helps operate the landing gear and brakes. This is completely normal during taxiing."
- Climbing (below 10,000 ft): "You might feel a falling sensation as the pitch of the airplane adjusts. This is normal - we're safely climbing to our cruising altitude."
- Cruising (30,000+ ft): "We're at our cruising altitude. The smooth flight you're experiencing is thanks to the stable air at this height. You can relax and enjoy the journey."
- Takeoff: "We're taking off! You may feel pressed into your seat - this is completely normal and safe."

Use the exact values provided and keep responses concise (1-2 sentences), very reassuring, and educational."""


@app.get("/api/flight/{flight_id}/calming-message", tags=["AI", "Flight"])
async def get_calming_message(flight_id: str):
    """
    Get an AI-generated calming message based on LIVE flight data.
    
    Fetches real-time flight information and generates a personalized
    calming message for anxious passengers.
    
    Args:
        flight_id: Flight number or callsign
    
    Returns:
        Calming message with live flight context
    """
    try:
        # Get LIVE flight data from FlightRadar24
        flight_data = await get_flight_info(flight_id)
        
        if flight_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Flight '{flight_id}' not found. The flight may not be currently active."
            )
        
        # Extract live values
        altitude = flight_data.get('altitude_ft', 0)
        speed = flight_data.get('speed_knots', 0)
        origin = flight_data.get('departure_airport', 'Unknown')
        destination = flight_data.get('arrival_airport', 'Unknown')
        
        # Build context with LIVE data
        flight_context = f"""
LIVE Flight Status (real-time data from FlightRadar24):
- Flight Number: {flight_data.get('flight_number', 'Unknown')}
- Status: In Flight
- CURRENT ALTITUDE: {altitude} feet
- CURRENT SPEED: {speed} knots
- ORIGIN: {origin}
- DESTINATION: {destination}
- Position: ({flight_data.get('latitude', 0):.4f}, {flight_data.get('longitude', 0):.4f})
- Heading: {flight_data.get('direction', 0)}°
"""
        
        user_message = f"""{flight_context}

Generate a calming, informative message about this flight's current status.
Use these EXACT values: Altitude: {altitude} feet, Speed: {speed} knots.
The passenger is on a flight from {origin} to {destination}."""
        
        # Get AI calming response
        calming_message = await simple_chat(
            user_message=user_message,
            system_prompt=CALMING_SYSTEM_PROMPT
        )
        
        return {
            "flight_id": flight_id,
            "message": calming_message,
            "flight_data": flight_data
        }
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# =============================================================================
# Vercel Serverless Handler
# =============================================================================

handler = Mangum(app)
