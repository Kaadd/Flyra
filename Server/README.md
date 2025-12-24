# Flyra Server

A FastAPI server compatible with Vercel serverless functions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the Server directory:
```bash
API_KEY=your_aviation_stack_api_key_here
```

Get your API key from [Aviation Stack](https://aviationstack.com/)

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

## Notes

- The server uses Mangum to adapt FastAPI for AWS Lambda/Vercel serverless functions
- CORS is enabled for all origins (adjust in production as needed)
- The handler is exported as `handler` for Vercel to use
- Flight data is fetched from Aviation Stack API
- Make sure to set your `API_KEY` in the `.env` file or as an environment variable in Vercel

