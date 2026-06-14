import socket
import time
import sys
import math

PROXY_HOST = '127.0.0.1'
PROXY_PORT = 8080
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9000

def run_tcp(path):
    print(f"[*] Sending TCP HTTP GET Request for {path} via Proxy...\n")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PROXY_HOST, PROXY_PORT))
        
        # Raw HTTP Request
        request = f"GET {path} HTTP/1.1\r\nHost: {PROXY_HOST}\r\nConnection: close\r\n\r\n"
        s.sendall(request.encode())
        
        response = b""
        while True:
            data = s.recv(4096)
            if not data: break
            response += data
            
        print(response.decode('utf-8', errors='ignore'))
    except Exception as e:
        print(f"[!] TCP Error: {e}")
    finally:
        s.close()

def run_udp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1.0) # Batas timeout 1 detik sesuai modul
    
    rtts = []
    sent = 10
    lost = 0
    
    print(f"[*] Mengirim {sent} paket UDP (Ping QoS) ke {SERVER_HOST}:{SERVER_PORT}...\n")
    
    for i in range(1, sent + 1):
        send_time = time.time()
        message = f"Ping {i} {send_time}"
        
        try:
            s.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
            data, addr = s.recvfrom(1024)
            recv_time = time.time()
            
            rtt_ms = (recv_time - send_time) * 1000
            rtts.append(rtt_ms)
            print(f"Reply from {addr[0]}: seq={i} time={rtt_ms:.2f} ms")
        except socket.timeout:
            lost += 1
            print(f"Request timed out for seq={i}")
            
    print("\n" + "="*30)
    print("      HASIL ANALISIS QoS      ")
    print("="*30)
    
    if rtts:
        min_rtt = min(rtts)
        max_rtt = max(rtts)
        avg_rtt = sum(rtts) / len(rtts)
        
        # Jitter: Deviasi standar selisih RTT berturut-turut σ(ΔRTT)
        jitter = 0
        if len(rtts) > 1:
            diffs = [abs(rtts[j] - rtts[j-1]) for j in range(1, len(rtts))]
            mean_diff = sum(diffs) / len(diffs)
            variance = sum((d - mean_diff) ** 2 for d in diffs) / len(diffs)
            jitter = math.sqrt(variance)
            
        print(f"Latency (RTT) : Min = {min_rtt:.2f} ms | Max = {max_rtt:.2f} ms | Avg = {avg_rtt:.2f} ms")
        print(f"Jitter        : {jitter:.2f} ms")
    
    loss_pct = (lost / sent) * 100
    print(f"Packet Loss   : {loss_pct:.1f}% ({lost}/{sent} lost)")
    print("="*30)
    
    s.close()

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
        
    if len(sys.argv) < 3 or sys.argv[1] != "--mode":
        print("Penggunaan:")
        print("  python client.py --mode tcp [path_url] [proxy_host] [proxy_port]")
        print("  python client.py --mode udp [server_host] [server_port]")
        sys.exit(1)
        
    mode = sys.argv[2].lower()
    
    if mode == "tcp":
        path = sys.argv[3] if len(sys.argv) > 3 else "/"
        if len(sys.argv) > 4:
            PROXY_HOST = sys.argv[4]
        if len(sys.argv) > 5:
            try:
                PROXY_PORT = int(sys.argv[5])
            except ValueError:
                pass
        run_tcp(path)
    elif mode == "udp":
        if len(sys.argv) > 3:
            SERVER_HOST = sys.argv[3]
        if len(sys.argv) > 4:
            try:
                SERVER_PORT = int(sys.argv[4])
            except ValueError:
                pass
        run_udp()
    else:
        print("[!] Mode tidak valid. Gunakan 'tcp' atau 'udp'.")