import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5555


def get_time():
    return datetime.now().strftime("%H:%M")


def receive_messages(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                print("\nServer disconnected.")
                break

            print(f"\n{message.decode('utf-8')}")
            print("You: ", end="", flush=True)

        except ConnectionResetError:
            print("\nConnection closed by the server.")
            break

        except OSError:
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))

        print("=" * 50)
        print("          PYTHON CHAT APPLICATION")
        print("=" * 50)

        username = input("Enter your username: ").strip()

        if not username:
            username = "Guest"

        client.send(username.encode("utf-8"))

        receive_thread = threading.Thread(
            target=receive_messages,
            args=(client,),
            daemon=True
        )

        receive_thread.start()

        print("\nYou are connected!")
        print("Type your message and press Enter.")
        print("Type /quit to leave the chat.\n")

        while True:
            message = input("You: ").strip()

            if not message:
                continue

            client.send(message.encode("utf-8"))

            if message.lower() == "/quit":
                break

    except ConnectionRefusedError:
        print("\nCould not connect to the server.")
        print("Make sure server.py is running first.")

    except Exception as e:
        print(f"\nError: {e}")

    finally:
        client.close()
        print("\nDisconnected from chat.")


if __name__ == "__main__":
    start_client()