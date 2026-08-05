import socket

SERVER_PORT = 5050
BUFFER_SIZE = 16
ENCODING = 'utf-8'
DISCONNECT_SIGNAL = "False"

server_hostname = socket.gethostname()
server_ip = socket.gethostbyname(server_hostname)
server_address = (server_ip, SERVER_PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen()

print(f"Server is running on {server_ip}:{SERVER_PORT}")
print("Waiting for a client to connect...\n")

while True:
    connection, client_address = server_socket.accept()
    print(f"Connected to client: {client_address}")
    
    connected = True
    while connected:
        
        raw_msg_length = connection.recv(BUFFER_SIZE).decode(ENCODING)
        
        if raw_msg_length:
            msg_length = int(raw_msg_length.strip())
            
            message = connection.recv(msg_length).decode(ENCODING)
            
            if message == DISCONNECT_SIGNAL:
                connection.send("Goodbye!".encode(ENCODING))
                print("Client disconnected.")
                connected = False
            else:
                
                print(f"Client says: {message}")
                
                vowels = "aeiouAEIOU"
                vowel_count = 0
                for letter in message:
                    if letter in vowels:
                        vowel_count += 1
                
                if vowel_count == 0:
                    reply = "Not enough vowels"
                elif vowel_count <= 2:
                    reply = "Enough vowels I guess"
                else:
                    reply = "Too many vowels"
                
                connection.send(reply.encode(ENCODING))
                
    connection.close()