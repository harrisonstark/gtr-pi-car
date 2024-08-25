import asyncio
from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from routes import event
from src.routes import healthcheck, stream_video
from src.utils.mongo import poll_mongo
from src.utils.events import start_event_processor

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
    # Start the MongoDB poller and event processor on startup
    asyncio.create_task(poll_mongo())
    start_event_processor()

# Include the routes from the imported endpoint modules
app.include_router(event.router)
app.include_router(healthcheck.router)
app.include_router(stream_video.router)