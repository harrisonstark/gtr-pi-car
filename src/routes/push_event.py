from fastapi import APIRouter, Request
from src.utils.globals import globals_instance

router = APIRouter()

@router.post("/push_event")
async def push_event(request: Request):
    globals_instance.event_queue.put(request.query_params.get("event"))
    return {"status": 200}