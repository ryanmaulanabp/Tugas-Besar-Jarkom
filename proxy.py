import socket
import threading
import os
import hashlib
import time
from datetime import datetime

PROXY_PORT = 8080
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000
CACHE_DIR = './proxy_cache'

# Membuat direktori cache jika belum ada
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def handle_client(client_socket, client_addr):
    start_time = time.time()
    try:
        request = client_socket.recv(4096)
        if not request: return
        
        req_str = request.decode('utf-8', errors='ignore')
        first_line = req_str.split('\r\n')[0]
        url = first_line.split()[1] if len(first_line.split()) > 1 else ""

        # Membuat Cache Key dengan Hash MD5 dari URL
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(CACHE_DIR, cache_key)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Cek Cache (CACHE HIT)
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                client_socket.sendall(f.read())
            
            elapsed = (time.time() - start_time) * 1000
            print(f"[{now}] PROXY - Client: {client_addr[0]} | URL: {url} | Cache: HIT | Time: {elapsed:.2f}ms")
        
        # Request ke Server Asli (CACHE MISS)
        else:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(5.0) # 5 seconds timeout
            try:
                server_socket.connect((SERVER_HOST, SERVER_PORT))
                server_socket.sendall(request)
                
                response = b""
                while True:
                    data = server_socket.recv(4096)
                    if not data: break
                    response += data
                
                if response:
                    # Simpan raw response ke cache
                    with open(cache_path, 'wb') as f:
                        f.write(response)
                    client_socket.sendall(response)
                    
                elapsed = (time.time() - start_time) * 1000
                print(f"[{now}] PROXY - Client: {client_addr[0]} | URL: {url} | Cache: MISS | Time: {elapsed:.2f}ms")
                
            except socket.timeout:
                print(f"[{now}] ERROR 504 Gateway Timeout")
                client_socket.sendall(b"HTTP/1.1 504 Gateway Timeout\r\nContent-Type: text/html\r\n\r\n<h1>504 Gateway Timeout</h1>")
            except Exception as e:
                print(f"[{now}] ERROR 502 Bad Gateway: {e}")
                client_socket.sendall(b"HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/html\r\n\r\n<h1>502 Bad Gateway</h1>")
            finally:
                server_socket.close()

    except Exception as e:
        print(f"[PROXY] Connection Error: {e}")
    finally:
        client_socket.close()

def start_proxy():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind(('0.0.0.0', PROXY_PORT))
    proxy.listen(20)
    print(f"[*] Proxy Server listening on Port {PROXY_PORT}")
    
    while True:
        client, addr = proxy.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    start_proxy()