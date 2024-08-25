from queue import Queue
import logging
import threading
import time
from src.utils.globals import globals_instance

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

def process_events():
    while True:
        if not globals_instance.event_queue.empty():
            globals_instance.current_event = globals_instance.event_queue.get()
            # TODO: process events with C code for GPIO
        else:
            globals_instance.current_event = None
        time.sleep(1)  # Process every second

def start_event_processor():
    event_processor_thread = threading.Thread(target=process_events)
    event_processor_thread.start()