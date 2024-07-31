import socket
import ssl
import threading

HOST = '0.0.0.0'
PORT = 8080

def handle_client(conn, addr):
    
    while True:
        try:
            # Receive message from client
            message = conn.recv(1024).decode()

            # Broadcast the message to all clients
            for client in clients:
                client.send(message.encode())
        except:
            # Remove the client from the list if there's an error
            index = clients.index(conn)
            clients.remove(conn)
            conn.close()
            print(f"Connection closed: {addr}")
            break

def start_server():
    """
    Function to start the server and listen for incoming connections.
    """
    # Start listening for incoming connections
    ssl_socket.listen()

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Wait for a client to connect
        conn, addr = ssl_socket.accept()
        clients.append(conn)

        print(f"Connection established: {addr}")

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, 8080))

# Load SSL/TLS certificate and key
certfile = "server.crt"
keyfile = "server.key"
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile, keyfile)

# Wrap the socket with SSL/TLS
ssl_socket = ssl_context.wrap_socket(server_socket, server_side=True)

if __name__ == "__main__":
    start_server()
