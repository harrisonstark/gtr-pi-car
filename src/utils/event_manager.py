import threading
import time
from src.utils.globals import globals_instance

def process_events():
    while True:
        if not globals_instance.event_queue.empty():
            globals_instance.current_event = globals_instance.event_queue.get()
            # TODO: process events with C code for GPIO
            time.sleep(1) # remove this and wait for the event to finish processing
        else:
            globals_instance.current_event = None
            time.sleep(1)

def start_event_processor():
    globals_instance.event_processing_thread = threading.Thread(target=process_events)
    globals_instance.event_processing_thread.start()

def stop_event_processor():
    globals_instance.event_processing_thread.join()