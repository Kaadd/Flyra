# Flyra Server

A FastAPI server for real-time flight tracking and calming assistance, compatible with Vercel serverless functions.

## Features

- **Real-time flight tracking** using FlightRadar24 API
- **AI-powered calming messages** for anxious passengers
- **Live position data** including altitude, speed, and coordinates
- Serverless deployment on Vercel

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the Server directory:
```bash
# FlightRadar24 API token (required for flight data)
FLIGHTRADARAPI_KEY=your_flightradar24_api_token_here

# OpenAI API key (required for AI calming messages)
OPENAI_KEY=your_openai_api_key_here
```

Get your API keys from:
- [FlightRadar24 API](https://fr24api.flightradar24.com/docs)
- [OpenAI](https://platform.openai.com/)

## Local Development

To run locally (for testing before deploying):

```bash
uvicorn api.index:app --reload
```

Or using FastAPI CLI:
```bash
fastapi dev api/index.py
```

## Testing

Run the test suite:
```bash
python test_flight_api.py
```

## Deployment to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Set environment variables in Vercel:
```bash
vercel env add FLIGHTRADARAPI_KEY
vercel env add OPENAI_KEY
```

3. Deploy:
```bash
vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.

## API Endpoints

### Health & Info
- `GET /` - Root endpoint with API info
- `GET /health` - Health check

### Flight Tracking (Live Data)
- `GET /api/flight?flight_id={flight_number}` - Get LIVE flight information
  - Example: `/api/flight?flight_id=UA837`
  - Returns real-time altitude, speed, position, and route data
  
- `GET /api/flights/search?departure={IATA}&arrival={IATA}` - Search flights by route
  - Example: `/api/flights/search?departure=JFK&arrival=LAX`

### AI Calming Assistant
- `GET /api/flight/{flight_id}/calming-message` - Get AI-generated calming message with live flight context
- `POST /api/ai/chat` - General AI chat endpoint

## Data Source

All flight data is **live** from [FlightRadar24](https://www.flightradar24.com/). No mock data is used.

The API returns:
- `altitude_ft`: Current altitude in feet
- `speed_knots`: Ground speed in knots
- `latitude` / `longitude`: Current position
- `direction`: Heading in degrees
- `departure_airport` / `arrival_airport`: Route information
- `is_live`: Always `true` (indicates real-time data)
- `data_source`: Always `"flightradar24"`

## Architecture

```
Server/
├── api/
│   ├── index.py              # FastAPI app & endpoints
│   ├── flight_service.py     # Flight data service (uses FlightRadar24)
│   ├── ai_service.py         # OpenAI integration
│   └── flightDataApi/        # FlightRadar24 API wrapper
│       ├── __init__.py
│       ├── flight_data_interface.py
│       └── flightRadar24API.py
├── requirements.txt
├── vercel.json
└── README.md
```

## Notes

- The server uses Mangum to adapt FastAPI for AWS Lambda/Vercel serverless functions
- CORS is enabled for all origins (adjust in production as needed)
- The handler is exported as `handler` for Vercel to use
- **All flight data is LIVE from FlightRadar24** - no mock data
- Rate limits may apply based on your FlightRadar24 API plan
