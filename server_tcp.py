import socket

def reverse_message(message):
    return message[::-1]

def start_server():
    # Define server address and port
    server_address = '127.0.0.1'  # localhost
    server_port = 65432

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_socket.bind((server_address, server_port))

    # Listen for incoming connections (maximum 1 connection in the queue)
    server_socket.listen(1)
    print(f"Server listening on {server_address}:{server_port}")

    # Wait for a connection
    conn, client_address = server_socket.accept()
    with conn:
        print(f"Connected to {client_address}")
        
        # Receive data from the client
        data = conn.recv(1024).decode()
        if data:
            print(f"Received: {data}")
            
            # Process the received data (reverse the message)
            response = reverse_message(data)
            print(f"Sending response: {response}")
            
            # Send the processed data back to the client
            conn.sendall(response.encode())
        else:
            print("No data received")
    
    # Close the socket
    server_socket.close()

if __name__ == '__main__':
    start_server()
