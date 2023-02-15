import threading
import time

# create class, that has a integer counter, a start and stop method for the thread and a increment method, finally a method to get the counter value

class Counter:
    def __init__(self):
        self.counter = 0
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()

    def increment(self):
        self.counter += 1

    def get_counter(self):
        return self.counter

    def run(self):
        while True:
            self.increment()
            print(f"Counter (module): {self.get_counter()}")
            time.sleep(1)