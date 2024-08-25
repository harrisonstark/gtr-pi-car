import cv2
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from src.utils.logger import configure_logging

# Set up custom logger for error logging
log = configure_logging()

router = APIRouter()

def gen_frames():
    """Generate frames from the webcam."""
    cap = cv2.VideoCapture(0)  # 0 is usually the default camera
    if not cap.isOpened():
        log.error("Unable to open webcam")
        raise RuntimeError("Could not start video capture")

    while True:
        success, frame = cap.read()
        if not success:
            log.error("Failed to capture frame")
            break

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            log.error("Failed to encode frame")
            break

        # Convert the encoded frame to bytes and yield
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@router.get("/stream_video")
async def stream_video(request: Request):
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
