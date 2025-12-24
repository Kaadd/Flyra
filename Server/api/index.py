from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

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
    # Mock data
    return {
        "flight_id": flight_id,
        "flight_number": flight_id.upper(),
        "flight_status": "On time",
        "flight_time": "10:00 AM",
        "flight_date": "2025-01-01",
        "flight_gate": "A1",
        "flight_terminal": "1",
    }

# Vercel serverless handler
handler = Mangum(app)

