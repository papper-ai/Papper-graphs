from threading import Event


class CancellationToken:
    def __init__(self):
        self.cancel_event = Event()

    def cancel(self):
        self.cancel_event.set()

    def is_cancelled(self):
        return self.cancel_event.is_set()
