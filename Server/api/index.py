from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from .flight_service import get_flight_info
from .ai_service import simple_chat, chat_completion


class ChatRequest(BaseModel):
    message: str
    system_message: Optional[str] = None

app = FastAPI(title="Flyra API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Flyra API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from Flyra API!"}

@app.post("/api/ai/chat")
async def ai_chat(request: ChatRequest):
    """
    Simple AI chat endpoint.
    
    Args:
        request: ChatRequest with message and optional system_message
    
    Returns:
        AI response
    """
    try:
        response = await simple_chat(
            user_message=request.message,
            system_message=request.system_message
        )
        return {"response": response}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI service error: {str(e)}"
        )

@app.get("/api/flight")
async def flight(flight_id: str):
    """
    Get flight information from Aviation Stack API.
    
    Args:
        flight_id: Flight number (e.g., "UA837", "AA100")
    
    Returns:
        Flight information dictionary
    """
    try:
        flight_data = await get_flight_info(flight_id)
        
        if flight_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Flight {flight_id} not found"
            )
        
        return flight_data
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/flight/{flight_id}/calming-message")
async def flight_calming_message(flight_id: str):
    """
    Get a calming and informative message about the flight status.
    
    Args:
        flight_id: Flight number (e.g., "UA837", "AA100")
    
    Returns:
        Dictionary with flight info and AI-generated calming message
    """
    try:
        # Get flight information
        flight_data = await get_flight_info(flight_id)
        
        if flight_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Flight {flight_id} not found"
            )
        
        # Build context for AI
        raw_data = flight_data.get("raw_data", {})
        flight_info = raw_data.get("flight", {})
        departure = raw_data.get("departure", {})
        arrival = raw_data.get("arrival", {})
        aircraft = raw_data.get("aircraft", {})
        
        # Extract relevant information
        flight_status = flight_data.get("flight_status", "unknown")
        aircraft_type = aircraft.get("iata", "") or aircraft.get("icao24", "") or "aircraft"
        departure_airport = departure.get("airport", "") or departure.get("iata", "")
        arrival_airport = arrival.get("airport", "") or arrival.get("iata", "")
        departure_delay = departure.get("delay")
        
        # Build flight context string
        flight_context = f"""
Flight Information:
- Flight Number: {flight_data.get('flight_number', flight_id)}
- Status: {flight_status}
- Aircraft Type: {aircraft_type}
- Departure Airport: {departure_airport}
- Arrival Airport: {arrival_airport}
- Scheduled Time: {flight_data.get('flight_time', 'TBD')}
- Gate: {flight_data.get('flight_gate', 'TBD')}
- Terminal: {flight_data.get('flight_terminal', 'TBD')}
"""
        
        if departure_delay:
            flight_context += f"- Departure Delay: {departure_delay} minutes\n"
        
        # Add any additional flight phase information if available
        if raw_data.get("live"):
            live_data = raw_data.get("live", {})
            altitude = live_data.get("altitude")
            speed = live_data.get("speed")
            direction = live_data.get("direction")
            
            if altitude:
                flight_context += f"- Current Altitude: {altitude} feet\n"
            if speed:
                flight_context += f"- Current Speed: {speed} km/h\n"
            if direction:
                flight_context += f"- Direction: {direction}°\n"
        
        # Create system message for AI
        system_message = """You are a flight calming assistant. I'm going to give you information about a flight's current status, and you are going to give me a sentence or two that is both informative and calming. 

Your responses should:
- Explain what's happening in simple, reassuring terms
- Use technical terms when helpful but explain them clearly
- Be calming and reassuring
- Be concise (1-2 sentences)
- Focus on normal, safe operations

Examples:
- If the flight is taxiing: "The scrubbing noise you might have heard is coming from the PTU (Power Transfer Unit). The PTU is a normal part of the aircraft's hydraulic system that helps maintain pressure - it's completely safe and expected during taxiing."
- If at altitude 7000 feet: "You might feel a falling sensation around 10,000 feet - this is completely normal. The pitch of the airplane is going down because we've safely completed takeoff and are now gradually climbing to our cruising altitude."
- If delayed: "We're experiencing a brief delay, which gives our crew extra time to ensure everything is perfectly prepared for a safe and comfortable flight."
- If on time: "Everything is proceeding smoothly. The aircraft is ready and we're on schedule for an on-time departure."
"""
        
        user_message = f"Here is the current flight information:\n{flight_context}\n\nPlease provide a calming and informative message about this flight's status."
        
        # Generate calming message
        calming_message = await simple_chat(
            user_message=user_message,
            system_message=system_message,
            model="gpt-3.5-turbo"
        )
        
        return {
            "flight_info": {
                "flight_number": flight_data.get("flight_number"),
                "flight_status": flight_data.get("flight_status"),
                "flight_time": flight_data.get("flight_time"),
                "flight_date": flight_data.get("flight_date"),
                "flight_gate": flight_data.get("flight_gate"),
                "flight_terminal": flight_data.get("flight_terminal"),
            },
            "calming_message": calming_message
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating calming message: {str(e)}"
        )

# Vercel serverless handler
handler = Mangum(app)

