from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import threading
import time
from datetime import datetime
import os

# ---------- Try to import real packet capture library ----------
try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("[WARNING] Scapy not installed. Falling back to simulated packets.")
    print("          For real capture: pip install scapy")
    print("          On Linux/macOS you may need sudo. On Windows install Npcap.")

app = Flask(__name__)
CORS(app)

# Global variables
packets_data = []
monitoring = False
monitoring_thread = None
capture_lock = threading.Lock()  # optional, for thread-safe list access

# Port to service mapping (same as before)
PORT_SERVICE = {
    80: 'HTTP', 443: 'HTTPS', 53: 'DNS', 22: 'SSH', 21: 'FTP',
    25: 'SMTP', 110: 'POP3', 143: 'IMAP', 3306: 'MySQL', 3389: 'RDP',
    8080: 'HTTP-ALT', 8443: 'HTTPS-ALT', 123: 'NTP', 161: 'SNMP',
    67: 'DHCP', 68: 'DHCP', 20: 'FTP-DATA', 23: 'TELNET', 993: 'IMAPS',
    995: 'POP3S', 5432: 'PostgreSQL', 27017: 'MongoDB'
}

def get_service(port):
    """Map port to service name"""
    try:
        if port == '-':
            return 'ICMP'
        return PORT_SERVICE.get(int(port), f'Port-{port}')
    except:
        return 'Unknown'

# ---------- Real packet callback (used when Scapy is available) ----------
def process_real_packet(packet):
    """Extract data from a live packet and add it to packets_data"""
    global packets_data

    if not monitoring:
        return  # stop adding packets when monitoring is off

    # Only handle IP packets
    if not packet.haslayer(IP):
        return

    ip_layer = packet[IP]
    timestamp = datetime.now().strftime('%H:%M:%S')
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    size = len(packet)

    # Determine protocol and ports
    if packet.haslayer(TCP):
        protocol = 'TCP'
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        protocol = 'UDP'
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    elif packet.haslayer(ICMP):
        protocol = 'ICMP'
        src_port = '-'
        dst_port = '-'
    else:
        # Non-IP, non-TCP/UDP/ICMP – skip or handle as 'OTHER'
        return

    service = get_service(dst_port)

    new_packet = {
        'time': timestamp,
        'src_ip': src_ip,
        'src_port': src_port,
        'dst_ip': dst_ip,
        'dst_port': dst_port,
        'protocol': protocol,
        'service': service,
        'size': size
    }

    with capture_lock:
        packets_data.append(new_packet)
        # Keep only last 200 packets
        if len(packets_data) > 200:
            packets_data = packets_data[-200:]

# ---------- Simulation fallback (same as original) ----------
def generate_initial_packets(count=50):
    """Generate initial packet data (used for simulation mode only)"""
    protocols = ['TCP', 'UDP', 'ICMP']
    src_ips = ['192.168.1.5', '192.168.1.10', '192.168.1.15', '192.168.1.20', 
               '192.168.1.25', '10.0.0.2', '10.0.0.5', '172.16.0.10']
    dst_ips = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '208.67.222.222', 
               '31.13.79.246', '142.250.185.46', '151.101.65.140']
    
    packets = []
    current_time = datetime.now()
    
    for i in range(count):
        protocol = random.choice(protocols)
        
        if protocol == 'TCP':
            dst_port = random.choice([80, 443, 53, 22, 25, 3306, 3389, 8080, 21])
            src_port = random.randint(1024, 65535)
            size = random.randint(40, 1500)
        elif protocol == 'UDP':
            dst_port = random.choice([53, 67, 68, 123, 161, 5060])
            src_port = random.randint(1024, 65535)
            size = random.randint(32, 1400)
        else:  # ICMP
            dst_port = '-'
            src_port = '-'
            size = random.randint(64, 1000)
        
        time_offset = i * random.randint(1, 3)
        timestamp = current_time.timestamp() - time_offset
        time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
        
        packets.append({
            'time': time_str,
            'src_ip': random.choice(src_ips),
            'src_port': src_port,
            'dst_ip': random.choice(dst_ips),
            'dst_port': dst_port,
            'protocol': protocol,
            'service': get_service(dst_port),
            'size': size
        })
    
    return packets

def simulation_worker():
    """Original background thread that simulates packets (fallback)"""
    global packets_data, monitoring
    while monitoring:
        protocol = random.choice(['TCP', 'UDP', 'ICMP'])
        
        if protocol == 'TCP':
            dst_port = random.choice([80, 443, 53, 22, 25, 3306])
            src_port = random.randint(1024, 65535)
            size = random.randint(40, 1500)
        elif protocol == 'UDP':
            dst_port = random.choice([53, 123, 161, 67])
            src_port = random.randint(1024, 65535)
            size = random.randint(32, 1400)
        else:
            dst_port = '-'
            src_port = '-'
            size = random.randint(64, 1000)
        
        new_packet = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'src_ip': f"192.168.1.{random.randint(2, 50)}",
            'src_port': src_port,
            'dst_ip': random.choice(['8.8.8.8', '1.1.1.1', '208.67.222.222', '31.13.79.246']),
            'dst_port': dst_port,
            'protocol': protocol,
            'service': get_service(dst_port),
            'size': size
        }
        
        with capture_lock:
            packets_data.append(new_packet)
            if len(packets_data) > 200:
                packets_data = packets_data[-200:]
        
        time.sleep(2)

# ---------- Main monitoring thread (chooses real or simulation) ----------
def monitor_worker():
    """Starts either real packet sniffer or simulation based on Scapy availability"""
    global monitoring, packets_data

    if SCAPY_AVAILABLE:
        print("[INFO] Starting REAL packet capture on network interface...")
        print("       (Default interface: try 'eth0' or 'Wi-Fi'. May need sudo on Linux/macOS)")
        # Sniff packets – stop when monitoring becomes False
        sniff(prn=process_real_packet, store=False, stop_filter=lambda p: not monitoring)
    else:
        print("[INFO] Using simulation mode (Scapy not installed)")
        simulation_worker()

# ---------- Flask Routes (unchanged from your original) ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/packets')
def get_packets():
    return jsonify(packets_data)

@app.route('/api/stats')
def get_stats():
    if not packets_data:
        return jsonify({
            'total_packets': 0,
            'tcp_count': 0,
            'udp_count': 0,
            'icmp_count': 0,
            'avg_size': 0
        })
    
    total = len(packets_data)
    tcp = sum(1 for p in packets_data if p['protocol'] == 'TCP')
    udp = sum(1 for p in packets_data if p['protocol'] == 'UDP')
    icmp = sum(1 for p in packets_data if p['protocol'] == 'ICMP')
    avg_size = sum(p['size'] for p in packets_data) / total if total > 0 else 0
    
    return jsonify({
        'total_packets': total,
        'tcp_count': tcp,
        'udp_count': udp,
        'icmp_count': icmp,
        'avg_size': round(avg_size, 1)
    })

@app.route('/api/start', methods=['POST'])
def start_monitoring():
    global monitoring, monitoring_thread, packets_data
    
    if not monitoring:
        # Clear previous data when starting fresh
        with capture_lock:
            packets_data = []
            if not SCAPY_AVAILABLE:
                # Pre-populate with simulated initial packets if in fallback mode
                packets_data = generate_initial_packets(50)
        
        monitoring = True
        monitoring_thread = threading.Thread(target=monitor_worker, daemon=True)
        monitoring_thread.start()
        return jsonify({'status': 'success', 'message': 'Monitoring started'})
    
    return jsonify({'status': 'warning', 'message': 'Monitoring already active'})

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    global monitoring
    monitoring = False
    return jsonify({'status': 'success', 'message': 'Monitoring stopped'})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    global packets_data
    with capture_lock:
        packets_data = []
    return jsonify({'status': 'success', 'message': 'Data cleared'})

if __name__ == '__main__':
    print("="*60)
    print("NETWORK TRAFFIC MONITORING PLATFORM")
    print("="*60)
    if SCAPY_AVAILABLE:
        print("\n✓ REAL-TIME packet capture mode ENABLED")
        print("✓ Using Scapy to sniff network traffic")
        print("✓ Make sure to run with sufficient privileges:")
        print("    - Linux/macOS: sudo python app.py")
        print("    - Windows: Run as Administrator (with Npcap installed)")
    else:
        print("\n⚠ SIMULATION mode (install Scapy for real capture)")
        print("  pip install scapy")
    
    print("\n✓ Flask server starting...")
    print("✓ Open browser at: http://localhost:5000")
    print("✓ Click START to begin monitoring")
    print("\nPress CTRL+C to stop")
    print("="*60)
    app.run(debug=True, port=5000)
