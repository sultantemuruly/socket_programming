import socket
import threading
import pickle
from constants import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:
        msg_length_raw = conn.recv(HEADER)

        if msg_length_raw:
            try:
                msg_length = int(msg_length_raw.decode(FORMAT).strip())
                msg = conn.recv(msg_length)

                try:
                    msg_decoded = msg.decode(FORMAT)
                    print(f"[{addr}] [STRING MESSAGE]: {msg_decoded}")
                    if msg_decoded == DISCONNECT_MESSAGE:
                        connected = False
                    conn.send("Msg received".encode(FORMAT))
                except UnicodeDecodeError:
                    msg_object = pickle.loads(msg)
                    print(f"[{addr}] [OBJECT RECEIVED]: {msg_object}")
                    conn.send("Object received".encode(FORMAT))
            except ValueError:
                print(f"[{addr}] [INVALID MESSAGE LENGTH]")

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING]: server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]: {threading.active_count() - 1}")


print("[STARTING]: server is starting...")
start()
