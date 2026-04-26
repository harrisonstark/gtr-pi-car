from threading import Thread, Lock
import cv2

class ThreadedCamera:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.frame = None
        self.lock = Lock()
        self._running = True
        self.thread = Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self._running:
            if self.capture.isOpened():
                ok, frame = self.capture.read()
                if ok:
                    with self.lock:
                        self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self._running = False
        self.capture.release()