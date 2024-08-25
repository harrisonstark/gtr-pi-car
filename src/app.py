from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from src.routes import healthcheck, push_event, stream_video
from src.utils.event_manager import start_event_processor

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

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

# startup
@app.on_event("startup")
async def startup_event():
    start_event_processor()

# Include the routes from the imported endpoint modules
app.include_router(healthcheck.router)
app.include_router(push_event.router)
app.include_router(stream_video.router)