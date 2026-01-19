import socket
import ssl

def start_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the address (fixes "address already in use" error)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to localhost on port 5555
    host = '127.0.0.1'
    port = 8443  # Using 8443 for local HTTPS testing
    server_socket.bind((host, port))
    
    # Create SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    # Load certificate and private key
    # Rember to genrate them
    try:
        context.load_cert_chain('server.crt', 'server.key')
    except FileNotFoundError:
        print("ERROR: SSL certificate files not found!")
        print("\nTo generate self-signed certificate, run:")
        print("openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes")
        return
    
    # Listen for incoming connections
    server_socket.listen(5)
    print(f"SSL Server listening on {host}:{port}")
    
    while True:
        # Accept a client connection
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        
        # Wrap with SSL
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        
        try:
            while True:
                data = ssl_socket.recv(1024).decode('utf-8')
                
                if not data or data.lower() == 'quit':
                    print(f"Client {address} disconnected")
                    break
                
                print(f"Received: {data}")
                
                response = f"SSL Server received: {data}"
                ssl_socket.send(response.encode('utf-8'))
        
        except ssl.SSLError as e:
            print(f"SSL Error: {e}")
        finally:
            ssl_socket.close()

if __name__ == "__main__":
    start_server()