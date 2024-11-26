from dotenv import load_dotenv
load_dotenv()

import os
import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from route.api import api_router
from utils.state import initialize_backend_state

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

initialize_backend_state()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL"), "http://localhost:3000"],  # Add localhost for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response: {response.status_code}")
    return response

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app)