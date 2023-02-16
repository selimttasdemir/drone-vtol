import threading
import time
import multithreadingmodule


mult = multithreadingmodule.Counter()
mult.start()


# infinite loop, that prints the counter value every 5 seconds in multithreadingmodule.py
while True:
    print(f"Counter: {multithreadingmodule.Counter.get_counter(mult)}")
    time.sleep(5)