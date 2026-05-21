# Tugas Besar Jaringan Komputer: Client-Proxy-Server Socket Programming

Proyek ini adalah implementasi arsitektur jaringan **Client-Proxy-Server** menggunakan *socket programming* murni pada Python. Sistem ini mengevaluasi protokol TCP/UDP serta parameter *Quality of Service* (QoS) tanpa mengandalkan framework HTTP tingkat tinggi.

## 🚀 Fitur Utama

1. **Web Server Multithreading (`webserver.py`)**
   - **TCP HTTP Server (Port 8000):** Menangani *request* HTTP (GET) dan menyajikan berkas statis (HTML, CSS, Image, Video). Mendukung HTTP Status 200 OK dan 404 Not Found.
   - **UDP Echo Server (Port 9000):** Menerima *payload* dari klien dan memantulkannya kembali untuk keperluan kalkulasi *Latency* dan *Packet Loss*.
2. **Proxy Server Terdistribusi (`proxy.py`)**
   - Menerima *request* HTTP dari klien (Port 8080) dan meneruskannya ke Web Server.
   - **Sistem Caching:** Menggunakan *hash* MD5 dari URL untuk menyimpan respons server secara lokal. Jika URL yang sama diakses kembali (Cache HIT), *proxy* akan merespons langsung tanpa menghubungi Web Server.
   - **Error Handling Mandiri:** Mampu menghasilkan respons `502 Bad Gateway` dan `504 Gateway Timeout` jika Web Server mati atau tidak merespons.
3. **Client Simulator & QoS Analyzer (`client.py`)**
   - **Mode TCP:** Melakukan *fetch* HTTP melalui Proxy.
   - **Mode UDP:** Melakukan *ping* ke UDP Echo Server untuk menghitung **RTT (Min, Max, Avg)**, **Jitter**, dan **Packet Loss**.

## 📁 Struktur Direktori

```text
/Tugas_Besar_Jarkom
│── client.py
│── proxy.py
│── webserver.py
│── proxy_cache/       (Digenerate otomatis oleh proxy.py)
│── index.html         
│── osi.html
│── tcpip.html
│── qos.html
│── implementation.html
│── README.md
│── css/
│   └── style.css
│── assets/
│   ├── iflab.png
│   ├── network.png
│   ├── osi.png
│   ├── osi.mp4
│   └── tcpip.png
└── status/
    ├── 404.html
    ├── 500.html
    ├── 502.html
    └── 504.html
