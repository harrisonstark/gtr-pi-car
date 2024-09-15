from threading import Thread, Lock
import cv2
import time

class ThreadedCamera:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        
        self.frame = None
        self.status = None
        self.lock = Lock()

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        
    def update(self):
        while True:
            if self.capture.isOpened():
                self.status, self.frame = self.capture.read()
            
    def get_frame(self):
        return self.frame
