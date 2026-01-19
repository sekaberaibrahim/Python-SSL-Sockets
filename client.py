# client.py - SSL/TLS Client
import socket
import ssl

def start_client():
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to remote server
    host = '40.104.14.210'
    port = 443
    
    # Wrap socket with SSL/TLS
    context = ssl.create_default_context()
    
    # Disable certificate verification for testing (NOT recommended for production)
    # Use this when certificate doesn't match IP or is self-signed
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    print("⚠️  Warning: SSL certificate verification is DISABLED")
    
    try:
        # Wrap the socket with SSL
        ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
        ssl_socket.connect((host, port))
        print(f"SSL/TLS Connected to {host}:{port}")
        print(f"Cipher: {ssl_socket.cipher()}")
        print(f"Protocol: {ssl_socket.version()}")
        
        # Send HTTP request (since it's HTTPS)
        request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        ssl_socket.send(request.encode('utf-8'))
        
        # Receive response
        response = b""
        while True:
            data = ssl_socket.recv(4096)
            if not data:
                break
            response += data
        
        print("\nResponse received:")
        print(response.decode('utf-8', errors='ignore')[:500])  # Print first 500 chars
    
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except ConnectionRefusedError:
        print(f"Connection refused - server may not be running at {host}:{port}")
    except socket.timeout:
        print("Connection timed out")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssl_socket.close()
        print("\nConnection closed")

if __name__ == "__main__":
    start_client()