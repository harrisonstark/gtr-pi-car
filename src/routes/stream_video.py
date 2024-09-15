import time
import cv2
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from src.utils.globals import globals_instance
import logging
from src.utils.threaded_camera import ThreadedCamera

logger = logging.getLogger('uvicorn.error')
router = APIRouter()

cap = ThreadedCamera()

def gen_frames():
    while True:
        frame = cap.get_frame()
        if frame is None:
            logger.error("Failed to capture frame")
            continue

        frame = cv2.resize(frame, (240, 160))

        overlay_text = f"Current event: {globals_instance.current_event}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = .5
        color = (0, 0, 0)
        thickness = 2
        position = (5, 15)

        cv2.putText(frame, overlay_text, position, font, font_scale, color, thickness, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        if not ret:
            logger.error("Failed to encode frame")
            continue

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(.25)

@router.get("/stream_video")
async def stream_video(request: Request):
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
