import socket
import pickle

from constants import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


def send_object(obj):
    message = pickle.dumps(obj)  # Serialize the object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


test_msg = "Hello World!"
test_object = {"name": "Jake Williams", "age": 27, "hometown": "Nashville, Tennessee"}

send("Hello World!")
send_object(test_object)
send(DISCONNECT_MESSAGE)
