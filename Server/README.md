# Flyra Server

A FastAPI server compatible with Vercel serverless functions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the Server directory:
```bash
OPENAI_KEY=your_openai_api_key_here
```

Get your API key from [OpenAI](https://platform.openai.com/)

## Local Development

To run locally (for testing before deploying):

```bash
uvicorn api.index:app --reload
```

Or using FastAPI CLI:
```bash
fastapi dev api/index.py
```

## Deployment to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

Or connect your GitHub repository to Vercel for automatic deployments.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/hello` - Hello endpoint
- `GET /api/flight?flight_id={flight_number}` - Get flight information (e.g., `/api/flight?flight_id=UA837`)
- `GET /api/flight/{flight_id}/calming-message` - Get AI-generated calming message about flight
- `POST /api/ai/chat` - AI chat endpoint

## Notes

- The server uses Mangum to adapt FastAPI for AWS Lambda/Vercel serverless functions
- CORS is enabled for all origins (adjust in production as needed)
- The handler is exported as `handler` for Vercel to use
- Flight data uses mock/fake data (no external API required)
- Make sure to set your `OPENAI_KEY` in the `.env` file or as an environment variable in Vercel

