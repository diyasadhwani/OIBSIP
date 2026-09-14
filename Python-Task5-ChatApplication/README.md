# Python Chat Application

A beginner-level real-time chat application built with Python using socket programming and threading.

## Features

* Real-time messaging between connected clients
* Server handles multiple client connections
* Username support
* Timestamp displayed with every message
* Join notification when a user connects
* Disconnect notification when a user leaves
* Graceful disconnection using `/quit`
* Runs locally using localhost

## Technologies Used

* Python
* Socket Programming
* Threading
* DateTime

## Project Structure

```text
Python-Task5-ChatApplication/
│
├── server.py
├── client.py
└── README.md
```

## How to Run

### 1. Start the Server

Open a terminal in the project folder and run:

```bash
python server.py
```

The server will run on:

```text
127.0.0.1:5555
```

### 2. Start the First Client

Open a new terminal in the same folder and run:

```bash
python client.py
```

Enter a username when prompted.

### 3. Start the Second Client

Open another terminal and run:

```bash
python client.py
```

Enter another username.

Both clients can now communicate with each other in real time.

## Example

```text
[16:08] alice: hello bob
[16:08] bob: hi alice
```

When a user disconnects:

```text
[16:08] bob has disconnected.
```

## Commands

To leave the chat, type:

```text
/quit
```

## How It Works

The server uses a TCP socket to accept incoming client connections.

Each connected client is handled using a separate thread. This allows multiple clients to communicate with the server at the same time.

When a client sends a message, the server receives it and broadcasts it to the other connected clients. Messages are displayed with the sender's username and timestamp.

## Security Note

This project is created for educational purposes and runs on localhost.

Messages are transmitted through a normal TCP socket connection and are **not end-to-end encrypted**. The application does not implement authentication or encryption.

Therefore, this project should not be used to send sensitive or private information.

## Learning Resources

* Python Socket Documentation: https://docs.python.org/3/library/socket.html
* Python Threading Documentation: https://docs.python.org/3/library/threading.html
