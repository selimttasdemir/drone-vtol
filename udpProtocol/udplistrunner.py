import udplist
import time


obj = udplist.UdpListener(8000)
obj.start()

while True:
    print(obj.get_messages())
    time.sleep(5)