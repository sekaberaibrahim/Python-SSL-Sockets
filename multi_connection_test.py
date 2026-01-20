# Testing multiple IPs
import socket
import ssl

servers = [
    ('40.17.14.190', 443),
    ('52.13.43.5', 443),
    ('10.16.24.27', 443),
    ('19.23.45.16', 443),
]

def test_connection(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(5)
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        ssl_socket = context.wrap_socket(client_socket, server_hostname=host)
        ssl_socket.connect((host, port))
        
        print(f"✅ {host}:{port} - CONNECTED")
        ssl_socket.close()
        return True
        
    except Exception as e:
        print(f"❌ {host}:{port} - FAILED: {e}")
        return False

if __name__ == "__main__":
    print("Testing connections...\n")
    for host, port in servers:
        test_connection(host, port)
