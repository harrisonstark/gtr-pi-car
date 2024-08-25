import cv2
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from src.utils.logger import configure_logging
from src.utils.globals import globals_instance

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

         # Overlay text on the frame
        event_to_display = globals_instance.current_event if globals_instance.current_event == None else globals_instance.current_event["event"]
        overlay_text = f"Current event: {event_to_display}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 255, 0)  # Green color in BGR
        thickness = 2
        position = (10, 30)  # Top-left corner of the frame

        # Put the overlay text on the frame
        cv2.putText(frame, overlay_text, position, font, font_scale, color, thickness, cv2.LINE_AA)


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
