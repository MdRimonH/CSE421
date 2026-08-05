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

print(f"Salary Server is running on {server_ip}:{SERVER_PORT}")
print("Waiting for a client...\n")

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
                print(f"Client says hours worked: {message}")
                
               

                if message.isdigit():
                    hours = float(message) 
                    
                    if hours <= 40:
                        salary = hours * 200
                    else:
                        extra_hours = hours - 40
                        salary = 8000 + (extra_hours * 300)
                        
                    reply = f"The salary is Tk {salary}"
                else:
                    
                    reply = "Invalid input. Please send a whole number."
                
              
                connection.send(reply.encode(ENCODING))
                
    connection.close()