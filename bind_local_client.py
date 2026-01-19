# bind_local_client.py - Bind to your local IP
import socket
import ssl

local_ip = '10.178.77.205'  # Your IP
local_port = 0  # Let OS choose port

remote_ip = '40.104.14.210'
remote_port = 443

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind to your local IP (optional)
    client_socket.bind((local_ip, local_port))
    print(f"Bound to {local_ip}:{client_socket.getsockname()[1]}")
    
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    ssl_socket = context.wrap_socket(client_socket, server_hostname=remote_ip)
    ssl_socket.connect((remote_ip, remote_port))
    
    print(f"Connected to {remote_ip}:{remote_port}")
    print(f"Local address: {ssl_socket.getsockname()}")
    
    # Send request
    request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(remote_ip)
    ssl_socket.send(request.encode())
    
    response = ssl_socket.recv(4096)
    print(response.decode('utf-8', errors='ignore'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    client_socket.close()