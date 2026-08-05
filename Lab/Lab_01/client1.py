import socket

# Client configuration
SERVER_PORT = 5050
# How many bytes to read at once? We use 16 bytes for the length header because it’s small and fixed.
BUFFER_SIZE = 16
# Sockets send bytes, not strings. But we usually work with text.
ENCODING = 'utf-8'  
# “I’m done talking — please close the connection.”
DISCONNECT_SIGNAL = "False"

# Get client hostname and IP address
client_hostname = socket.gethostname()
client_ip = socket.gethostbyname(client_hostname)

print(f"Client Hostname: {client_hostname}")
print(f"Client IP Address: {client_ip}")

# Server address to connect to (using local server IP here)
server_address = (client_ip, SERVER_PORT)

# Create a TCP socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

def send_message(message):
    # Encode the message to bytes i.e string → bytes
    encoded_message = message.encode(ENCODING)
    
    # Prepare a fixed-length header for the message length (padded)
    message_length = str(len(encoded_message)).encode(ENCODING)
    padded_length = message_length + b' ' * (BUFFER_SIZE - len(message_length))
    
    # Send the length header first
    client_socket.send(padded_length)
    
    # Then send the actual message bytes
    client_socket.send(encoded_message)
    
    # Receive and print server response
    response = client_socket.recv(2048).decode(ENCODING)
    print(f"Server response: {response}")

# Prepare message with client's IP and hostname
intro_message = f"Client IP: {client_ip}, Client Name: {client_hostname}"

# Send the intro message
send_message(intro_message)

# Send disconnect signal to server
send_message(DISCONNECT_SIGNAL)

# Close the client socket
client_socket.close()
print("Disconnected from server.")
