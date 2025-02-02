import socket
import threading


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an external server (doesn't actually send data)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address


PORT = 5052
SERVER = get_local_ip()
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION]: {addr} connected.")

    connected = True
    while connected:
        msg_length_raw = conn.recv(HEADER).decode(FORMAT)

        if msg_length_raw:
            msg_length = len(msg_length_raw)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

        print(f"[{addr}] [{msg}]")

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
