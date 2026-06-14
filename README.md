# Tugas Besar Jaringan Komputer: Sistem Client-Proxy-Server
Implementasi dan Analisis Kinerja Sistem Client-Proxy-Server Berbasis Socket Programming (Python) -- Evaluasi Protokol TCP/UDP dan Parameter Quality of Service (QoS).

---

## 👥 Identitas Kelompok (Kelas IF-48-06 / Kelompok 01)
| Nama | NIM | Peran Utama |
|---|---|---|
| **Ryan Maulana Bagus Putra** | 103012430029 | Client Simulator (`client.py`), QoS Measurement & Report |
| **Azmi Hanif Fauzil Islami** | 103012420018 | Proxy Server (`proxy.py`), Caching Mechanism & Error Handling |
| **Muhammad Rafiul Izzah** | 103012430004 | Web Server (`webserver.py`), Static File Handling & Logging |

---

## 🚀 Fitur Utama

1. **Web Server Multithreading (`webserver.py`)**
   - **TCP HTTP Server (Port 8000):** Menangani *request* HTTP GET dan menyajikan berkas statis (HTML, CSS, Image, Video) dengan response `200 OK` dan `404 Not Found`.
   - **UDP Echo Server (Port 9000):** Memantulkan kembali paket ping QoS tanpa modifikasi untuk mengukur kinerja jaringan secara murni.

2. **Proxy Server Terdistribusi dengan Caching (`proxy.py`)**
   - Menerima request HTTP dari klien (Port 8080) dan meneruskannya ke Web Server.
   - **Mekanisme Caching (MD5):** Menggunakan *hash* MD5 dari URL sebagai key cache. Cache HIT merespons langsung dalam 2-5 ms.
   - **Error Handling:** Otomatis mendeteksi dan mengembalikan `502 Bad Gateway` (jika server mati) dan `504 Gateway Timeout` (jika server lambat merespons).

3. **Client Simulator & QoS Analyzer (`client.py`)**
   - **Mode TCP:** Melakukan *fetch* halaman web melalui Proxy.
   - **Mode UDP:** Melakukan ping 10 datagram ke UDP Echo Server untuk menghitung **RTT (Min/Avg/Max)**, **Jitter**, dan **Packet Loss**.

---

## 💻 Panduan Menjalankan Sistem (Multi-PC / Jaringan Wi-Fi Sama)

Sistem ini telah dimodifikasi agar dapat berjalan pada **3 PC terpisah** dalam satu jaringan Wi-Fi yang sama:

### Skenario Penyiapan:
* **PC 1 (Web Server):** Menjalankan `webserver.py` (Misalkan IP Wi-Fi PC 1 adalah `192.168.1.50`)
* **PC 2 (Proxy Server):** Menjalankan `proxy.py` (Misalkan IP Wi-Fi PC 2 adalah `192.168.1.60`)
* **PC 3 (Client):** Menjalankan `client.py`

---

### Langkah-Langkah Eksekusi:

#### Langkah 1: Jalankan Web Server di PC 1
Buka terminal di PC 1 dan jalankan:
```bash
python webserver.py
```
*Web Server akan mendeteksi IP Wi-Fi lokalnya secara otomatis dan menampilkannya di terminal.*

#### Langkah 2: Jalankan Proxy Server di PC 2
Buka terminal di PC 2 dan arahkan ke Web Server (IP PC 1):
```bash
# Format: python proxy.py [IP_Web_Server] [Port_Web_Server] [Port_Proxy]
python proxy.py 192.168.1.50 8000 8080
```
*Proxy akan mendeteksi IP Wi-Fi lokalnya dan bersiap mem-forward request ke PC 1.*

#### Langkah 3: Jalankan Client di PC 3
Buka terminal di PC 3 untuk melakukan pengujian:

* **Untuk Request Web (Mode TCP):**
  ```bash
  # Format: python client.py --mode tcp [Path_URL] [IP_Proxy] [Port_Proxy]
  python client.py --mode tcp /index.html 192.168.1.60 8080
  ```

* **Untuk Pengukuran QoS (Mode UDP):**
  ```bash
  # Format: python client.py --mode udp [IP_Web_Server] [Port_UDP_Echo]
  python client.py --mode udp 192.168.1.50 9000
  ```

---

## 📁 Struktur Direktori
```text
.
├── client.py
├── proxy.py
├── webserver.py
├── laporan.tex           (Laporan Akhir berformat LaTeX)
├── index.html         
├── osi.html
├── tcpip.html
├── qos.html
├── implementation.html
├── README.md
├── css/
│   └── style.css
├── assets/
│   ├── iflab.png
│   └── ...
└── status/
    ├── 404.html
    ├── 500.html
    ├── 502.html
    └── 504.html
```
