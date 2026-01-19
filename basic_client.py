# basic_client.py - Simple TCP client
import socket

host = '40.104.14.210'  # Change this to any IP from your list
port = 443

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((host, port))
    print(f"Connected to {host}:{port}")
    
    # Send data
    message = "Hello Server"
    client_socket.send(message.encode('utf-8'))
    
    # Receive response
    response = client_socket.recv(4096)
    print(f"Received: {response}")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()