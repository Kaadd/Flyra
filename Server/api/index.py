from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from .flight_service import get_flight_info

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

# Vercel serverless handler
handler = Mangum(app)

