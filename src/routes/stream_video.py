import asyncio
import cv2
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from src.utils.globals import globals_instance
from src.utils.threaded_camera import ThreadedCamera
# from ultralytics import YOLO
import logging

logger = logging.getLogger("uvicorn.error")
router = APIRouter()
cap = ThreadedCamera()
# model = YOLO("yolov8n.pt")
# uncomment all the commented code to get YOLO data on the frames

async def gen_frames(request: Request):
    while True:
        if await request.is_disconnected():
            break

        frame = cap.get_frame()
        if frame is None:
            await asyncio.sleep(0.05)
            continue

        # results = model(frame, verbose=False)
        # for box in results[0].boxes:
        #     x1, y1, x2, y2 = map(int, box.xyxy[0])
        #     conf = float(box.conf[0])
        #     cls = int(box.cls[0])
        #     label = f"{model.names[cls]} {conf:.2f}"
        #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #     cv2.putText(frame, label, (x1, y1 - 5),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.putText(frame, f"Event: {globals_instance.current_event}",
                    (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
        if not ret:
            continue

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
               + buffer.tobytes() + b'\r\n')

        await asyncio.sleep(1/30)

@router.get("/stream_video")
async def stream_video(request: Request):
    return StreamingResponse(gen_frames(request), media_type="multipart/x-mixed-replace; boundary=frame")