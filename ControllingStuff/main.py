from machine import Pin, ADC
import socket
from web_server import connect_wifi, send_json, serve_file

BUTTON_PIN = 15
LED_PIN = 16

button_pin = Pin(BUTTON_PIN, Pin.IN)
led_pin = Pin(LED_PIN, Pin.OUT)
temp_sensor = ADC(4)

# Connect to WiFi
connect_wifi()

# create a TCP socket for the web server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

def read_internal_temperature():
    # Read the raw ADC value
    adc_value = temp_sensor.read_u16()

    # Convert ADC value to voltage
    voltage = adc_value * (3.3 / 65535.0)

    # Temperature calculation based on sensor characteristics
    temperature_celsius = 27 - (voltage - 0.706) / 0.001721

    return temperature_celsius

while True:
    conn, addr = s.accept()
    print('Client connected from', addr)
    request = conn.recv(1024).decode()
    print('Request:', request)

    if 'GET / ' in request:
        serve_file(conn, 'index.html')
    elif 'GET /hardwareState' in request:
        send_json(conn, '200 OK', {
            'buttonState': not button_pin.value(),
            'cpuTemp': read_internal_temperature(),
        })
    elif 'GET /toggleLED' in request:
        led_pin.value(0 if led_pin.value() else 1)
        send_json(conn, '200 OK', {
            'ledState': led_pin.value(),
        })
    else:
        send_json(conn, '404 Not Found', {
            'error': 'Route not found',
        })
    
    conn.close()