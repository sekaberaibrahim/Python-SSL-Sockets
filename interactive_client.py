# Interactive SSL client
import socket
import ssl

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    try:
        ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
        ssl_socket.connect((host, port))
        print(f"✅ Connected to {host}:{port}")
        
        while True:
            message = input("\nEnter message (or 'quit'): ")
            if message.lower() == 'quit':
                break
            
            ssl_socket.send(message.encode('utf-8'))
            response = ssl_socket.recv(4096)
            print(f"Response: {response.decode('utf-8', errors='ignore')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    host = input("Enter IP address (default 40.104.14.210): ") or "40.104.14.210"
    port = int(input("Enter port (default 443): ") or "443")
    connect_to_server(host, port)