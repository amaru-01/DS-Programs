import socket
import threading
import time

# Network topology - define which processes are connected
connections = {
    0: [1, 2],  # Process 0 is connected to Process 1 and 2
    1: [0, 3],  # Process 1 is connected to Process 0 and 3
    2: [0, 4],  # Process 2 is connected to Process 0 and 4
    3: [1],     # Process 3 is connected to Process 1
    4: [2]      # Process 4 is connected to Process 2
}

# Define the address and port for each process
addresses = {
    0: ('127.0.0.1', 5000),
    1: ('127.0.0.1', 5001),
    2: ('127.0.0.1', 5002),
    3: ('127.0.0.1', 5003),
    4: ('127.0.0.1', 5004)
}

# Define the process (node) class
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.address = addresses[node_id]
        self.connections = connections[node_id]
        self.server_thread = threading.Thread(target=self.start_server)
        self.client_threads = []

    def start_server(self):
        """Start the server part of the process to receive messages."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.address)
        server_socket.listen(5)
        print(f"Node {self.node_id} listening on {self.address}")
        
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=self.handle_connection, args=(conn,)).start()

    def handle_connection(self, conn):
        """Handle incoming connection."""
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Node {self.node_id} received message: {data}")
        conn.close()

    def send_message(self, target_node, message):
        """Send a message to a target node."""
        target_address = addresses[target_node]
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(target_address)
        client_socket.sendall(message.encode())
        client_socket.close()

    def start_clients(self):
        """Start the clients that will send messages to connected nodes."""
        for target_node in self.connections:
            message = f"Hello from Node {self.node_id} to Node {target_node}"
            client_thread = threading.Thread(target=self.send_message, args=(target_node, message))
            client_thread.start()
            self.client_threads.append(client_thread)

    def start(self):
        """Start the node (both server and clients)."""
        self.server_thread.start()
        time.sleep(1)  # Allow server to start before clients send messages
        self.start_clients()

# Main function to start all nodes
def start_network():
    nodes = []
    for node_id in range(5):
        node = Node(node_id)
        nodes.append(node)
        node.start()

    # Join the client threads to ensure they finish before exiting
    for node in nodes:
        for client_thread in node.client_threads:
            client_thread.join()

# Start the process network
if __name__ == '__main__':
    start_network()
