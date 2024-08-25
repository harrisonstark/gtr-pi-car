from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import healthcheck, stream_video

app = FastAPI()

# Configure CORS
origins = ["https://gtr-pi.harrisonstark.net", "http://gtr-pi.harrisonstark.net", "http://localhost:7070"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes from the imported endpoint modules
app.include_router(healthcheck.router)
app.include_router(stream_video.router)