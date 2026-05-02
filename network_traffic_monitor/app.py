from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global variables
packets_data = []
monitoring = False
monitoring_thread = None

# dictionary for Port to service mapping
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

def generate_initial_packets(count=50):
    """Generate initial packet data"""
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
        
        # Create timestamp going backwards for realism
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

def monitor_worker():
    """Background thread to simulate packet capture"""
    global packets_data, monitoring
    
    packet_counter = len(packets_data)
    
    while monitoring:
        # Generate a new packet every 2 seconds
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
        
        packets_data.append(new_packet)
        packet_counter += 1
        
        # Keep only last 200 packets to avoid memory issues
        if len(packets_data) > 200:
            packets_data = packets_data[-200:]
        
        time.sleep(2)

@app.route('/')
def index():
    """Serve the index.html file"""
    return render_template('index.html')

@app.route('/api/packets')
def get_packets():
    """Return all packets - matches your frontend expected format"""
    return jsonify(packets_data)

@app.route('/api/stats')
def get_stats():
    """Return statistics - matches your frontend expected format"""
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
    """Start packet monitoring"""
    global monitoring, monitoring_thread, packets_data
    
    if not monitoring:
        # Generate initial 50 packets
        packets_data = generate_initial_packets(50)
        monitoring = True
        monitoring_thread = threading.Thread(target=monitor_worker, daemon=True)
        monitoring_thread.start()
        return jsonify({'status': 'success', 'message': 'Monitoring started'})
    
    return jsonify({'status': 'warning', 'message': 'Monitoring already active'})

@app.route('/api/stop', methods=['POST'])
def stop_monitoring():
    """Stop packet monitoring"""
    global monitoring
    monitoring = False
    return jsonify({'status': 'success', 'message': 'Monitoring stopped'})

@app.route('/api/clear', methods=['POST'])
def clear_data():
    """Clear all packet data"""
    global packets_data
    packets_data = []
    return jsonify({'status': 'success', 'message': 'Data cleared'})

if __name__ == '__main__':
    print("="*60)
    print("NETWORK TRAFFIC MONITORING PLATFORM")
    print("="*60)
    print("\n✓ Server starting...")
    print("✓ Make sure your index.html is in the 'templates' folder")
    print("✓ Open your web browser")
    print("✓ Go to: http://localhost:5000")
    print("✓ Click START to begin monitoring")
    print("\nPress CTRL+C to stop the server")
    print("="*60)
    app.run(debug=True, port=5000)