import socket
import threading
import time

# common variable between threads
udp_message = ""
udp_message_addr = ""
date = ""

# lock for synchronizing access to the shared variable
lock = threading.Lock()

def receive_udp_messages():
    # create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 8000))

    while True:
        data, addr = sock.recvfrom(1024)
        # acquire lock to update the shared variable
        with lock:
            global udp_message, udp_message_addr, date
            udp_message = data.decode()
            udp_message_addr = addr

            # get the current date
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        print(f"Received message: {udp_message} from {addr[0]}")

def print_udp_message():
    while True:
        # acquire lock to access the shared variable
        with lock:
            global udp_message
            message = udp_message

        if message:
            print("*" * 50)
            print(f"Message: {message} from {udp_message_addr[0]}")
            print(f"Date: {date}")
            time.sleep(1)

# create and start the receiving thread
receive_thread = threading.Thread(target=receive_udp_messages)
receive_thread.start()

# create and start the printing thread
print_thread = threading.Thread(target=print_udp_message)
print_thread.start()

# wait for both threads to finish
receive_thread.join()
print_thread.join()