# Flyra Server

A FastAPI server compatible with Vercel serverless functions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

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

## Notes

- The server uses Mangum to adapt FastAPI for AWS Lambda/Vercel serverless functions
- CORS is enabled for all origins (adjust in production as needed)
- The handler is exported as `handler` for Vercel to use

