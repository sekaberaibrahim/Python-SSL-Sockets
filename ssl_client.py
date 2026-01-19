# ssl_client.py - SSL/TLS client
import socket
import ssl

host = '40.104.14.210'
port = 443

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

try:
    ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
    ssl_socket.connect((host, port))
    print(f"SSL Connected to {host}:{port}")
    print(f"Cipher: {ssl_socket.cipher()}")
    
    # Send HTTP request
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    ssl_socket.send(request.encode('utf-8'))
    
    # Receive response
    response = b""
    while True: 
        data = ssl_socket.recv(4096)
        if not data:
            break
        response += data
    
    print(response.decode('utf-8', errors='ignore'))
    
except Exception as e:
    print(f"Error: {e}")
finally:
    ssl_socket.close()