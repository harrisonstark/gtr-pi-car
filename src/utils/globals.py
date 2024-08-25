from queue import Queue

# Global object
class Globals:
    def __init__(self):
        self.current_event = None
        self.event_queue = Queue()

globals_instance = Globals()