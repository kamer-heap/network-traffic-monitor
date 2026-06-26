<div align="center">

<!-- Animated Header -->
<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&weight=700&size=42&pause=800&color=00FF88&center=true&vCenter=true&width=700&height=80&lines=%E2%AC%A1+Network+Traffic+Monitor" alt="title" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=18&pause=500&color=4fc3f7&center=true&width=700&lines=Intercepting+packets+in+real+time...;TCP+%C2%B7+UDP+%C2%B7+ICMP+%E2%80%94+all+protocols+captured;Flask+%2B+Python+%2B+Vanilla+JS" alt="subtitle" />



</div>

</div>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://shields.io)
[![Scapy](https://img.shields.io/badge/Scapy-2.5%2B-FF8C00?style=for-the-badge&logo=python&logoColor=white)](https://shields.io)
[![Flask](https://img.shields.io/badge/Flask-2.x-FF6B6B?style=for-the-badge&logo=flask&logoColor=white)](https://shields.io)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://shields.io)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://shields.io)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://shields.io)
[![License](https://img.shields.io/badge/License-MIT-00C896?style=for-the-badge)](https://shields.io)
[![Status](https://img.shields.io/badge/Status-Active-7C3AED?style=for-the-badge)](https://shields.io)


</p>

> **⬡ A browser-based network traffic monitoring dashboard** that captures live traffic (real-time) or simulates packets, analyzes protocols, maps ports to services, and filters — all powered by a Flask REST API backend.

<br/>

</div>

---
## 📸 Dashboard Preview

### Main Dashboard
![Dashboard Preview](https://raw.githubusercontent.com/kamer-stack/network-traffic-monitor/main/network_traffic_monitor/assets/screenshot.jpg)


---

## 🧪 Simulation Mode

When Scapy is unavailable or insufficient privileges are detected, the application automatically switches to simulation mode.

![Simulation Mode](https://raw.githubusercontent.com/kamer-stack/network-traffic-monitor/main/network_traffic_monitor/assets/sim.png)

---

## 🌐 Real Packet Capture Mode

When Scapy is installed and run with required permissions, the dashboard captures real packets in real time.

![Real Packet Capture](https://raw.githubusercontent.com/kamer-stack/network-traffic-monitor/main/network_traffic_monitor/assets/real.png)

---
## 🌐 About the Project


The platform demonstrates core networking concepts through a fully functional, browser-based live dashboard:

- **Hybrid capture** — real-time packet sniffing (Scapy) with automatic fallback to intelligent simulation
-  **Live statistics** — tracks total packets, per-protocol counts, and average packet size
-  **Filtering** — filter traffic by protocol, source IP, or destination IP
-  **Activity logging** — timestamped log of all user actions and system events
-  **Clean REST API** — decoupled backend/frontend architecture using Flask

No external JavaScript frameworks. No paid tools. Just Python + a browser.

---

##  Features


| Feature | Description |
|---|---|
|  **Start / Stop Monitoring** | Toggle live packet capture (real or simulated) on/off |
|  **Live Packet Table** | View packets with time, source/destination IP & port, protocol, service, and size |
|  **Protocol Badges** | Color-coded badges for TCP (blue), UDP (orange), and ICMP (pink) |
|  **Statistics Bar** | Total packets, TCP/UDP/ICMP counts, and average packet size — all live |
|  **Smart Filtering** | Filter by protocol dropdown, source IP, or destination IP (partial match supported) |
|  **Clear Data** | Wipe all captured packets and reset statistics in one click |
|  **Activity Log** | Timestamped event log capped at 50 entries with FIFO rotation |
|  **Terminal Dark UI** | Fully responsive dark-theme interface with pulsing live indicator |
|  **20+ Port Mappings** | Maps well-known ports to service names (HTTP, SSH, DNS, MySQL, and more) |
| **Memory-Safe** | Packet buffer capped at 200 entries to prevent memory growth |

---
##  Real Capture vs Simulation Mode

| Mode | When used | Features |
|---|---|---|
| **Real mode** | Scapy installed + sufficient privileges | Sniffs actual network traffic from your interface – shows real IPs, ports, protocols |
| **Simulation mode** | Scapy missing or insufficient permissions | Generates realistic synthetic packets every 2 seconds – identical data structure, no special rights needed |

The system decides automatically at startup and prints a message in the terminal:
- `✓ REAL-TIME packet capture mode ENABLED`
- `⚠ SIMULATION mode (install Scapy for real capture)`

---
##  Tech Stack

### Backend
| Technology | Role |
|---|---|
| **Python 3** | Core backend language |
| **Scapy 2.5+** | Real-time packet sniffing from live network interface (fallback to random simulation if missing) |
| **Flask 2.x** | Web framework & REST API server |
| **Flask-CORS** | Enables cross-origin requests from the frontend |
| **threading** (stdlib) | Runs background packet generation as a daemon thread |
| **random** (stdlib) | Used only in simulation fallback mode |
| **datetime** (stdlib) | Timestamps for both real and simulated packets |

### Frontend
| Technology | Role |
|---|---|
| **HTML5** | Page structure — header, controls, stats bar, packet table, log |
| **CSS3** | Dark terminal theme, animations, responsive layout |
| **Vanilla JavaScript (ES6)** | Fetch API calls, auto-refresh timer, DOM updates, filtering |
| **Fetch API** | Async HTTP calls to Flask every 2 seconds |

### Communication
| Protocol | Purpose |
|---|---|
| **HTTP REST** | GET for data retrieval, POST for control actions |
| **JSON** | All API responses serialized and parsed natively |

---

##  Project Structure

```
network-traffic-monitor/
│
├── app.py                 # Flask backend — REST API + packet simulation engine
│
└── templates/
    └── index.html          # Frontend dashboard — single self-contained HTML file
```

> ⚠️ **Important:** `index.html` **must** be placed inside a folder named `templates/` for Flask to serve it correctly.

---

##  Quick Start

### Prerequisites

Make sure you have **Python 3** installed. Then install the required packages:

```bash
pip install flask flask-cors scapy
```
> **For real-time capture:**  
> - Linux/macOS: run with `sudo` (e.g., `sudo python app.py`)  
> - Windows: install [Npcap](https://npcap.com) and run terminal as Administrator  
> 
> **If Scapy is missing or permissions insufficient**, the system automatically falls back to **simulation mode** (no special rights needed). Both modes use the same frontend.
### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/network-traffic-monitor.git
cd network-traffic-monitor

# 2. Create the templates folder and move index.html into it
mkdir templates
mv index.html templates/

# 3. Run the Flask server
python app.py          # simulation mode if Scapy missing, or real capture if Scapy present
```
On Linux/macOS for real capture:
```bash

sudo python app.py
```


### Open in Browser

```
http://localhost:5000
```

### Usage

1. ** START** — begins monitoring: (real mode) starts sniffing live traffic; (simulation mode) generates 50 initial packets then adds one every 2 seconds
2. **STOP** — pauses packet generation (data is preserved)
3. ** CLEAR** — wipes all packet data and resets statistics
4. Use the **Filter Bar** to narrow results by protocol, source IP, or destination IP
5. Click ** RESET** to restore the full unfiltered view

---

##  API Reference

All endpoints are served at `http://localhost:5000`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend dashboard (`index.html`) |
| `POST` | `/api/start` | Starts packet capture (real mode or simulation fallback) – clears previous data |
| `POST` | `/api/stop` | Stops the background packet generation thread |
| `GET` | `/api/packets` | Returns the full packet list as a JSON array |
| `GET` | `/api/stats` | Returns aggregated stats: totals, protocol counts, average size |
| `POST` | `/api/clear` | Clears all packet data and resets the buffer |
>  This mapping applies to **both real captured packets** (from Scapy) and simulated packets.

### Example Response — `/api/stats`

```json
{
  "total_packets": 78,
  "tcp_count": 42,
  "udp_count": 21,
  "icmp_count": 15,
  "avg_size": 726.3
}
```

### Example Response — `/api/packets` (single entry)

```json
{
  "time": "10:35:21",
  "src_ip": "192.168.1.5",
  "src_port": 52341,
  "dst_ip": "8.8.8.8",
  "dst_port": 80,
  "protocol": "TCP",
  "service": "HTTP",
  "size": 512
}
```

---

## 🔌 Port-to-Service Mapping

The backend maps 20+ well-known port numbers to application-layer service names:

| Port | Service | Port | Service | Port | Service |
|---|---|---|---|---|---|
| 80 | HTTP | 443 | HTTPS | 53 | DNS |
| 22 | SSH | 21 | FTP | 25 | SMTP |
| 110 | POP3 | 143 | IMAP | 123 | NTP |
| 161 | SNMP | 3306 | MySQL | 3389 | RDP |
| 993 | IMAPS | 995 | POP3S | 8080 | HTTP-ALT |
| 8443 | HTTPS-ALT | 5432 | PostgreSQL | 27017 | MongoDB |
| 20 | FTP-DATA | 23 | TELNET | 67/68 | DHCP |
| — | ICMP | — | — | — | — |

> Unrecognized ports are displayed as `Port-{n}`. ICMP packets have no port and are labeled `ICMP`.

---
##  License

MIT License

Copyright (c) 2026 Khadija Amer (kamer-stack)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.*

---

##  Author

**Khadija Amer**  
GitHub: [@kamer-heap](https://github.com/kamer-heap)

---

##  Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!



<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=00ff88&height=100&section=footer" width="100%"/>

*Built with 💚 by Khadija Amer | PUCIT*

</div>
