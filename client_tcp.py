import socket

def start_client():
    # Define server address and port
    server_address = '127.0.0.1'  # localhost
    server_port = 65432

    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_address, server_port))
        print(f"Connected to server at {server_address}:{server_port}")
        
        # Input message to send to server
        message = input("Enter message to send to server: ")
        
        # Send the message to the server
        client_socket.sendall(message.encode())
        
        # Wait for the response from the server
        response = client_socket.recv(1024).decode()
        print(f"Response from server: {response}")

    finally:
        # Close the socket
        client_socket.close()

if __name__ == '__main__':
    start_client()
