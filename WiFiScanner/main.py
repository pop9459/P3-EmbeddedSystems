import time
import network
import socket
try:
    import ujson as json
except ImportError:
    import json
from secrets import SSID, PASSWORD

# enable station interface and connect to WiFi access point
nic = network.WLAN(network.WLAN.IF_STA)
nic.active(True)

# Connect to WiFi (if not already connected)
if not nic.isconnected():
    print('Connecting to WiFi...')
    nic.connect(SSID, PASSWORD)
    # wait for connection (timeout after ~15 seconds)
    timeout = 15
    while not nic.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

if nic.isconnected():
    print('Connected, network config:', nic.ifconfig())
else:
    print('Failed to connect to WiFi. Check SSID/PASSWORD')

# create a TCP socket for the web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


def send_response(conn, status, content_type, body):
    conn.send(('HTTP/1.1 {}\r\n'.format(status)).encode())
    conn.send(('Content-Type: {}\r\n'.format(content_type)).encode())
    conn.send('Connection: close\r\n\r\n'.encode())
    conn.send(body.encode())


def scan_networks_payload(nic):
    networks = nic.scan()
    networks.sort(key=lambda x: x[3], reverse=True)  # sort by RSSI (signal strength)

    rows = []
    for index, net in enumerate(networks, start=1):
        ssid = net[0].decode('utf-8') if isinstance(net[0], bytes) else str(net[0])
        if not ssid:
            ssid = '(hidden)'
        rows.append({'nr': index, 'ssid': ssid, 'rssi': net[3]})

    return json.dumps({'ok': True, 'networks': rows})


def load_index_html():
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except Exception as e:
        return '<h1>index.html missing</h1><p>{}</p>'.format(e)

while True:
    conn, addr = s.accept()
    request_raw = conn.recv(1024)
    request_line = request_raw.decode('utf-8', 'ignore').split('\r\n')[0]
    request_parts = request_line.split(' ')
    path = request_parts[1] if len(request_parts) > 1 else '/'

    if path == '/':
        html = load_index_html()
        send_response(conn, '200 OK', 'text/html', html)
    elif path.startswith('/scan'):
        try:
            payload = scan_networks_payload(nic)
            send_response(conn, '200 OK', 'application/json', payload)
        except Exception as e:
            error_payload = json.dumps({'ok': False, 'error': str(e), 'networks': []})
            send_response(conn, '500 Internal Server Error', 'application/json', error_payload)
    else:
        send_response(conn, '404 Not Found', 'text/plain', 'Not Found')

    conn.close()
    # (optional) small delay to give the WiFi chip a breather
    time.sleep(1)