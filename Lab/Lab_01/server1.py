import socket

# Server configuration
SERVER_PORT = 5050
# How many bytes to read at once? We use 16 bytes for the length header because it’s small and fixed.
BUFFER_SIZE = 16
# Sockets send bytes, not strings. But we usually work with text.
ENCODING = 'utf-8'  
# “I’m done talking — please close the connection.”
DISCONNECT_SIGNAL = "False"

# Get server hostname and IP address
server_hostname = socket.gethostname()
server_ip = socket.gethostbyname(server_hostname)

print(f"Server Hostname: {server_hostname}")
print(f"Server IP Address: {server_ip}")

# Define server socket address tuple (IP, port)
server_address = (server_ip, SERVER_PORT)

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Start listening for incoming connections (default backlog)
server_socket.listen()

print(f"Server is running and listening on {server_ip}:{SERVER_PORT}")

while True:
    # Accept an incoming client connection where 'connection' is a new socket object used to communicate with the connected client.
    connection, client_address = server_socket.accept()
    print(f"Connection established with client: {client_address}")

    connected = True
    while connected:
        # Receive the fixed-length header indicating message length
        raw_msg_length = connection.recv(BUFFER_SIZE).decode(ENCODING)
        print(f"Raw message length from the client: {raw_msg_length}")
        if raw_msg_length:
            # Convert the length header to an integer
            msg_length = int(raw_msg_length.strip())
            
            # Receive the actual message based on the length
            message = connection.recv(msg_length).decode(ENCODING)
            
            if message == DISCONNECT_SIGNAL:
                # Client wants to disconnect
                connection.send("Goodbye!".encode(ENCODING))
                print("Client requested disconnect. Closing connection.")
                connected = False
            else:
                # Print the received message and send acknowledgment
                print(f"Received message: {message}")
                connection.send(f"Server received: {message}".encode(ENCODING))

    # Close the client socket after disconnect
    connection.close()
    print("Closed connection with client.\n")
    #break  # Exit the server loop for this example (remove for continuous server)
