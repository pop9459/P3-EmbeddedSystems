import time
import network
import socket
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

while True:
    conn, addr = s.accept()
    request = str(conn.recv(1024))
    
    if(request.find('/scan') != -1):
        # perform a scan and return results as HTML
        conn.send('HTTP/1.1 200 OK\n'.encode())
        conn.send('Content-Type: text/html\n'.encode())
        conn.send('Connection: close\n\n'.encode())
        conn.send('<html><body><h1>Available WiFi Networks</h1><ul>'.encode())
        conn.send("<table>\n".encode())
        conn.send("<tr>\n".encode())
        conn.send("<th>Nr</th><th>SSID</th><th>RSSI</th>\n".encode())
        conn.send("</tr>\n".encode())
        
        try:
            networks = nic.scan()
            networks.sort(key=lambda x: x[3], reverse=True)  # sort by RSSI (signal strength)
            for index, net in enumerate(networks, start=1):
                ssid = net[0].decode('utf-8') if isinstance(net[0], bytes) else str(net[0])
                conn.send(('<tr><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(index, ssid, net[3])).encode())
        except Exception as e:
            conn.send(('<tr><td colspan="3">Error scanning: {}</td></tr>\n'.format(e)).encode())
        conn.send("</table>\n".encode())
        conn.send('</body></html>'.encode())
        for testint in range(1, 6):
            conn.send(testint)
            time.sleep(0.5)
    else:
        conn.send('HTTP/1.1 404 Not Found\n'.encode())
        conn.send('Content-Type: text/html\n'.encode())
        conn.send('Connection: close\n\n'.encode())
    
    conn.close()
    # (optional) small delay to give the WiFi chip a breather
    time.sleep(1)