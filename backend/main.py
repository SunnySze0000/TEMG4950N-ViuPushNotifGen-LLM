from dotenv import load_dotenv
load_dotenv()

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.api import api_router
from utils.state import initialize_backend_state

app = FastAPI()

initialize_backend_state()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins = [os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
