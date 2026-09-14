import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555

clients = {}
lock = threading.Lock()


def get_time():
    return datetime.now().strftime("%H:%M")


def broadcast(message, sender=None):
    with lock:
        disconnected_clients = []

        for client in clients:
            if client != sender:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    disconnected_clients.append(client)

        for client in disconnected_clients:
            remove_client(client)


def remove_client(client):
    username = clients.get(client)

    if client in clients:
        del clients[client]

    try:
        client.close()
    except:
        pass

    if username:
        message = f"[{get_time()}] {username} has disconnected."
        print(message)
        broadcast(message)


def handle_client(client, address):
    try:
        username = client.recv(1024).decode("utf-8").strip()

        if not username:
            username = f"User-{address[1]}"

        with lock:
            clients[client] = username

        print(f"{username} connected from {address}")

        welcome = (
            f"[{get_time()}] Welcome {username}! "
            "You are connected to the chat."
        )
        client.send(welcome.encode("utf-8"))

        broadcast(
            f"[{get_time()}] {username} joined the chat.",
            client
        )

        while True:
            data = client.recv(1024)

            if not data:
                break

            message = data.decode("utf-8").strip()

            if message.lower() == "/quit":
                break

            if message:
                formatted_message = (
                    f"[{get_time()}] {username}: {message}"
                )

                print(formatted_message)
                broadcast(formatted_message, client)

    except ConnectionResetError:
        pass
    except Exception as e:
        print(f"Error with {address}: {e}")
    finally:
        remove_client(client)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(2)

    print("=" * 50)
    print("       PYTHON CHAT APPLICATION SERVER")
    print("=" * 50)
    print(f"Server running on {HOST}:{PORT}")
    print("Waiting for clients...")
    print("Press Ctrl+C to stop the server.")
    print("=" * 50)

    try:
        while True:
            client, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:
        print("\nServer stopped.")

    finally:
        with lock:
            for client in clients:
                try:
                    client.close()
                except:
                    pass

        server.close()


if __name__ == "__main__":
    start_server()
