from queue import Queue

# Global object
class Globals:
    def __init__(self):
        self.current_event = None
        self.event_queue = Queue()
        self.event_processing_thread = None

globals_instance = Globals()