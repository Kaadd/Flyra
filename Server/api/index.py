from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
from .flight_service import get_flight_info
from .ai_service import simple_chat

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


class ChatRequest(BaseModel):
    message: str
    system_prompt: str = None


@app.post("/api/ai/chat")
async def ai_chat(request: ChatRequest):
    """
    AI chat endpoint.
    
    Args:
        request: ChatRequest with message and optional system_prompt
    
    Returns:
        AI response
    """
    try:
        response = await simple_chat(
            user_message=request.message,
            system_prompt=request.system_prompt
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
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/flight/{flight_id}/calming-message")
async def get_calming_message(flight_id: str):
    """
    Get AI-generated calming message based on flight information.
    
    Args:
        flight_id: Flight number (e.g., "UA837", "AA100")
    
    Returns:
        Calming message with flight context
    """
    try:
        # Get flight data
        flight_data = await get_flight_info(flight_id)
        
        if flight_data is None:
            raise HTTPException(
                status_code=404,
                detail=f"Flight {flight_id} not found"
            )
        
        # Get actual values from flight data at the time button is pressed
        altitude = flight_data.get('altitude_ft')
        speed = flight_data.get('speed_mph')
        origin = flight_data.get('departure_airport', 'Unknown')
        destination = flight_data.get('arrival_airport', 'Unknown')
        status = flight_data.get('flight_status', 'Unknown')
        
        # Build context for AI with explicit values - these are the EXACT values at button press time
        flight_context = f"""
Current Flight Status (exact values at this moment):
- Flight Number: {flight_data.get('flight_number', 'Unknown')}
- Status: {status}
- Aircraft Type: {flight_data.get('aircraft_type', 'Unknown')}
- CURRENT ALTITUDE: {altitude} feet
- CURRENT SPEED: {speed} mph
- ORIGIN: {origin}
- DESTINATION: {destination}
- ETA: {flight_data.get('eta', 'Unknown')}
- Distance Remaining: {flight_data.get('distance_miles', 'Unknown')} miles
"""
        
        system_prompt = """You are a flight calming assistant. Your job is to reassure passengers that everything is fine and normal. Be very calming, reassuring, and emphasize that everything is operating normally.

IMPORTANT: 
- You MUST use the EXACT altitude and speed values provided (do not make up numbers)
- Always reassure that everything is fine and normal
- Keep it brief (1-2 sentences)
- Be very calming and reassuring

Examples:
- If the flight is taxiing: "The scrubbing noise you might've heard is coming from the PTU. The PTU is the Power Transfer Unit, which helps operate the landing gear and brakes. This is completely normal during taxiing."
- At altitude 7000 feet: "You might feel a falling sensation around 10000 feet, this is normal. The pitch of the airplane is going down because we are safely done with takeoff and we are slowly climbing to our cruising altitude."
- At cruising altitude: "We're now at our cruising altitude of [altitude] feet. The smooth flight you're experiencing is thanks to the stable air at this height. You can relax and enjoy the journey."
- Takeoff: "We're now taking off. you may feel like youre being pressed into your seat, this is normal."
Use the exact values provided and keep responses concise (1-2 sentences), very reassuring, and educational."""
        
        user_message = f"{flight_context}\n\nGenerate a calming, informative message about this flight's current status. Use these EXACT values: Altitude: {altitude} feet, Speed: {speed} mph, Origin: {origin}, Destination: {destination}."
        
        # Get AI response
        try:
            calming_message = await simple_chat(
                user_message=user_message,
                system_prompt=system_prompt
            )
        except ValueError as e:
            # OpenAI key missing or invalid
            raise HTTPException(
                status_code=400,
                detail=f"AI service error: {str(e)}"
            )
        except Exception as e:
            # Other OpenAI API errors
            raise HTTPException(
                status_code=500,
                detail=f"AI service error: {str(e)}"
            )
        
        return {
            "flight_id": flight_id,
            "message": calming_message,
            "flight_data": flight_data
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
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


# Vercel serverless handler
handler = Mangum(app)

