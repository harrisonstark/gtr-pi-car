import asyncio
import cv2
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from src.utils.globals import globals_instance
from src.utils.threaded_camera import ThreadedCamera
import logging

logger = logging.getLogger("uvicorn.error")
router = APIRouter()
cap = ThreadedCamera()

async def gen_frames(request: Request):
    while True:
        if await request.is_disconnected():
            break

        frame = cap.get_frame()
        if frame is None:
            await asyncio.sleep(0.05)
            continue

        cv2.putText(frame, f"Event: {globals_instance.current_event}",
                    (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        if not ret:
            continue

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
               + buffer.tobytes() + b'\r\n')

        await asyncio.sleep(1/30)  # target 30fps, non-blocking

@router.get("/stream_video")
async def stream_video(request: Request):
    return StreamingResponse(gen_frames(request), media_type="multipart/x-mixed-replace; boundary=frame")