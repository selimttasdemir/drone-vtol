import threading
import socket
import time
import json

# create a class that listens for UDP messages and stores them in a list. class instance can be started and stopped for listening for UDP messages. messages will be in json format. list will contain a dictionary with the id, longtitude, latitude, status (1 = finished, 0 = not finished) and the time the message was received

class UdpListener:
    def __init__(self, port: int,listBuffer=100):
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.udp_messages = [0 for i in range(listBuffer)]
        self.port = port

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()

    def run(self):
        # create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("0.0.0.0", self.port))

        while True:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            message["received_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.udp_messages[message["id"]] = message
            print(f"Received message: {message} from {addr[0]}")

    def get_messages(self):
        return self.udp_messages
    
    def get_message(self, id):
        return self.udp_messages[id]


