import socket
import threading
import os
from datetime import datetime

TCP_PORT = 8000
UDP_PORT = 9000
WEB_ROOT = '.'  # Root directory sejajar dengan webserver.py

def get_mime_type(filepath):
    ext = filepath.split('.')[-1].lower()
    mimes = {
        'html': 'text/html; charset=utf-8',
        'css': 'text/css',
        'png': 'image/png',
        'mp4': 'video/mp4'
    }
    return mimes.get(ext, 'application/octet-stream')

def handle_tcp_client(client_socket, addr):
    try:
        request = client_socket.recv(4096).decode('utf-8', errors='ignore')
        if not request: return
        
        headers = request.split('\r\n')
        first_line = headers[0].split()
        if len(first_line) < 2: return
        
        method, path = first_line[0], first_line[1]
        if path == '/': path = '/index.html'
        
        filepath = WEB_ROOT + path
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Handle 200 OK
        if os.path.exists(filepath) and not os.path.isdir(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()
            mime_type = get_mime_type(filepath)
            response_header = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type}\r\nContent-Length: {len(content)}\r\n\r\n".encode()
            client_socket.sendall(response_header + content)
            print(f"[{now}] TCP - IP: {addr[0]} | Path: {path} | Status: 200 OK")
        
        # Handle 404 Not Found
        else:
            error_path = os.path.join(WEB_ROOT, 'status', '404.html')
            if os.path.exists(error_path):
                with open(error_path, 'rb') as f: content = f.read()
            else:
                content = b"<h1>404 Not Found</h1>"
            response_header = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(content)}\r\n\r\n".encode()
            client_socket.sendall(response_header + content)
            print(f"[{now}] TCP - IP: {addr[0]} | Path: {path} | Status: 404 Not Found")

    except Exception as e:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] TCP Error: {e}")
    finally:
        client_socket.close()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def start_tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', TCP_PORT))
    server.listen(10)
    print(f"[*] TCP Web Server listening on Port {TCP_PORT} (HTTP)")
    print(f"[*] Connect to this server using IP: {get_local_ip()}")
    
    while True:
        client, addr = server.accept()
        # Multithreading per connection
        threading.Thread(target=handle_tcp_client, args=(client, addr), daemon=True).start()

def start_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', UDP_PORT))
    print(f"[*] UDP Echo Server listening on Port {UDP_PORT} (QoS Ping)")
    
    while True:
        data, addr = server.recvfrom(1024)
        server.sendto(data, addr)  # Echo back payload

if __name__ == "__main__":
    threading.Thread(target=start_udp_server, daemon=True).start()
    start_tcp_server()