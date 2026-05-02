<div align="center">

<!-- Animated Header -->
<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&weight=700&size=42&pause=800&color=00FF88&center=true&vCenter=true&width=700&height=80&lines=%E2%AC%A1+Network+Traffic+Monitor" alt="title" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=18&pause=500&color=4fc3f7&center=true&width=700&lines=Intercepting+packets+in+real+time...;TCP+%C2%B7+UDP+%C2%B7+ICMP+%E2%80%94+all+protocols+captured;Flask+%2B+Python+%2B+Vanilla+JS" alt="subtitle" />



</div>

</div>

<!-- Badges -->
<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![License](https://img.shields.io/badge/License-MIT-00ff88?style=for-the-badge)](LICENSE)

<p align="center">

[![Status](https://img.shields.io/badge/Status-Active-00ff88?style=for-the-badge)]()
[![Course](https://img.shields.io/badge/Course-CS--301%20Networks-blueviolet?style=for-the-badge)]()

</p>

> **⬡ A browser-based network traffic monitoring dashboard** that simulates real-time packet capture, protocol analysis, port-to-service mapping, and live filtering — all powered by a Flask REST API backend.

<br/>

</div>

---

## 🌐 About the Project

The **Network Traffic Monitoring and Analysis Platform** is an individual project developed for the **Computer Networks (CS-301)** course at **Punjab University College of Information Technology (PUCIT), University of the Punjab, Lahore**.

The platform demonstrates core networking concepts through a fully functional, browser-based live dashboard:

- 🔄 **Real-time packet simulation** — generates TCP, UDP, and ICMP packets dynamically every 2 seconds
- 📊 **Live statistics** — tracks total packets, per-protocol counts, and average packet size
- 🔍 **Filtering** — filter traffic by protocol, source IP, or destination IP
- 📜 **Activity logging** — timestamped log of all user actions and system events
- 🧩 **Clean REST API** — decoupled backend/frontend architecture using Flask

No external JavaScript frameworks. No paid tools. Just Python + a browser.

---

## ✨ Features

| Feature | Description |
|---|---|
| ▶️ **Start / Stop Monitoring** | Toggle real-time packet capture on and off |
| 📦 **Live Packet Table** | View packets with time, source/destination IP & port, protocol, service, and size |
| 🏷️ **Protocol Badges** | Color-coded badges for TCP (blue), UDP (orange), and ICMP (pink) |
| 📈 **Statistics Bar** | Total packets, TCP/UDP/ICMP counts, and average packet size — all live |
| 🔎 **Smart Filtering** | Filter by protocol dropdown, source IP, or destination IP (partial match supported) |
| 🗑️ **Clear Data** | Wipe all captured packets and reset statistics in one click |
| 🖥️ **Activity Log** | Timestamped event log capped at 50 entries with FIFO rotation |
| 🌙 **Terminal Dark UI** | Fully responsive dark-theme interface with pulsing live indicator |
| 🔌 **20+ Port Mappings** | Maps well-known ports to service names (HTTP, SSH, DNS, MySQL, and more) |
| 💾 **Memory-Safe** | Packet buffer capped at 200 entries to prevent memory growth |

---

## 🛠️ Tech Stack

### Backend
| Technology | Role |
|---|---|
| **Python 3** | Core backend language |
| **Flask 2.x** | Web framework & REST API server |
| **Flask-CORS** | Enables cross-origin requests from the frontend |
| **threading** (stdlib) | Runs background packet generation as a daemon thread |
| **random** (stdlib) | Generates realistic randomized packet values |
| **datetime** (stdlib) | Produces `HH:MM:SS` timestamps per packet |

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

## 📁 Project Structure

```
network-traffic-monitor/
│
├── app.py                  # Flask backend — REST API + packet simulation engine
│
└── templates/
    └── index.html          # Frontend dashboard — single self-contained HTML file
```

> ⚠️ **Important:** `index.html` **must** be placed inside a folder named `templates/` for Flask to serve it correctly.

---

## 🚀 Quick Start

### Prerequisites

Make sure you have **Python 3** installed. Then install the required packages:

```bash
pip install flask flask-cors
```

### Installation & Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/network-traffic-monitor.git
cd network-traffic-monitor

# 2. Create the templates folder and move index.html into it
mkdir templates
mv index.html templates/

# 3. Run the Flask server
python app.py
```

### Open in Browser

```
http://localhost:5000
```

### Usage

1. **▶ START** — begins monitoring and generates 50 initial packets, then adds one new packet every 2 seconds
2. **■ STOP** — pauses packet generation (data is preserved)
3. **✕ CLEAR** — wipes all packet data and resets statistics
4. Use the **Filter Bar** to narrow results by protocol, source IP, or destination IP
5. Click **↺ RESET** to restore the full unfiltered view

---

## 📡 API Reference

All endpoints are served at `http://localhost:5000`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend dashboard (`index.html`) |
| `POST` | `/api/start` | Starts packet simulation (generates 50 initial + continuous stream) |
| `POST` | `/api/stop` | Stops the background packet generation thread |
| `GET` | `/api/packets` | Returns the full packet list as a JSON array |
| `GET` | `/api/stats` | Returns aggregated stats: totals, protocol counts, average size |
| `POST` | `/api/clear` | Clears all packet data and resets the buffer |

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


<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=00ff88&height=100&section=footer" width="100%"/>

*Built with 💚 | PUCIT, University of the Punjab*

</div>
