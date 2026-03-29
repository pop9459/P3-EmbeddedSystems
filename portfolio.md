# Digital portfolio Embedded systems Y1 P3
-  Name: Peter Kapsiar
- Student ID: 5486866
- Repository: https://github.com/pop9459/P3-EmbeddedSystems/

## Blink with hardware reset
### Description
This is a simple test that blinks an LED on and off. With this we can verify that the microcontroller works properly. It also displays how to use an external hardware reset button to reset the microcontroller.

The code first imports the libraries for pin controll and time functions. It defines the 
output pins for the LEDs. In this case I used one external LED and also the picos built in LED. After that it just enters in a loop where it turns the leds on and off with some delays in between.

Components used:
- 1x RPI Pico W
- 1x LED
- 1x 10KΩ resistor
- push button

### Schematic
![schematic](./BlinkWithExternalHardwareReset/schematic.png)

### Code
`main.py`
```python
from machine import Pin
import utime

led_builtin = Pin("LED", Pin.OUT)
led_external = Pin(15, Pin.OUT)

while True:
    led_builtin.high()
    led_external.high()
    utime.sleep_ms(200)
    
    led_builtin.low()
    led_external.low()
    utime.sleep_ms(800)
```

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/output.JPEG)

## Mario pico

### Description
A short practice program that draws a pyramid shape to the output terminal using printable characters. It defines one variable at the begining which controlls the size of the pyramid drawing. For the first pyramid I just use a single character. It starts drawing it from the top so each line will get N "#" symbols on the N-th line. The second pyramid works on the same principle but prints diffenet symbols based on if it is printing the edge of the pyramid or the middle part.

Components used:
- 1x RPI Pico W

### Schematic
Not applicable for this project since it only prints to the console.

### Code
`main.py`
```python
pyramidSize = 10

for y in range(pyramidSize):
    for x in range(pyramidSize):
        if x < pyramidSize - y - 1:
            print(" ", end="")
        else:
            print("# ", end="")
    print()

for y in range(pyramidSize):
    for x in range(pyramidSize):
        if x < pyramidSize - y - 1:
            print(" ", end="")
        else:
            if y == 0:
                print("^", end="")
            elif x == pyramidSize - y - 1:
                print("/#", end="")
            elif x == pyramidSize - 1:
                print("\\ ", end="")
            else:
                print("##", end="")
    print()

```

### Output
![console output](/MarioPico/output.png)

## 7-Segments Voltmeter (0..10V)

### Description
This project uses a voltage divider to measure voltages from 0 to 10V using the Pico's ADC which can only measure up to 3.3V. The voltage is then displayed on a 4-digit 7-segment display. 

In the code the rpi calculates the voltage by multiplying the ADC reading by the voltage divider ratio. The voltage is then displayed on the 4-digit 7-segment display using a custom library that I created for controlling the display.

To controll the display the code uses a technique called multiplexing. This means that it turns on one digit at a time and sets the segments for that digit. It does this very quickly so that it appears that all digits are on at the same time. This is done to reduce the number of pins needed to control the display. To turn on a digit it connects the common cathode of that digit to ground using one of the transistors. The segments are then controlled by setting the corresponding pins high or low. To streamline this process the library has a predefined list of the segment values for each digit from 0 to 9. The library also has a function to write a value to the display which takes care of the multiplexing and segment control.

Components used:
- 1x RPI Pico W
- 1x 4-digit 7-segment display
- 5x 10KΩ resistor
- 1x 4.7KΩ resistor
- 8x 220Ω resistor
- 4x BC547C transistor 

### Schematic
![schematic](./7SegmentVoltmeter/schematic.png)

### Code
`main.py`
```python
from segment_display import Display
from machine import Pin, ADC
import time

# Display pin definitions
DISPLAY_DIGIT_1_PIN = 2
DISPLAY_DIGIT_2_PIN = 3
DISPLAY_DIGIT_3_PIN = 4
DISPLAY_DIGIT_4_PIN = 5
DISPLAY_SEGMENT_A_PIN = 6
DISPLAY_SEGMENT_B_PIN = 7
DISPLAY_SEGMENT_F_PIN = 8
DISPLAY_SEGMENT_E_PIN = 16
DISPLAY_SEGMENT_D_PIN = 17
DISPLAY_SEGMENT_C_PIN = 18
DISPLAY_SEGMENT_G_PIN = 19
DISPLAY_SEGMENT_DP_PIN = 20

# Voltmeter pin definition
VOLT_METER_PIN = 26
VOLTAGE_DIVIDER_RATIO = 3.127659574 # Calculated as (R1 + R2) / R2, where R1 = 10kΩ and R2 = 4.7kΩ

# Initialize the display
display = Display(
    DISPLAY_DIGIT_1_PIN,
    DISPLAY_DIGIT_2_PIN,
    DISPLAY_DIGIT_3_PIN,
    DISPLAY_DIGIT_4_PIN,
    DISPLAY_SEGMENT_A_PIN,
    DISPLAY_SEGMENT_B_PIN,
    DISPLAY_SEGMENT_C_PIN,
    DISPLAY_SEGMENT_D_PIN,
    DISPLAY_SEGMENT_E_PIN,
    DISPLAY_SEGMENT_F_PIN,
    DISPLAY_SEGMENT_G_PIN,
    DISPLAY_SEGMENT_DP_PIN,
)

# Initialize the voltmeter
voltmeter = ADC(Pin(VOLT_METER_PIN, Pin.IN))

# Main loop variables
update_delay_ms = 250
next_update_time = time.ticks_ms()
voltage = 0

while True:
    current_time = time.ticks_ms()

    display.write_value(voltage*100, dp=1)

    if time.ticks_diff(current_time, next_update_time) >= 0:
        voltage = (voltmeter.read_u16() / 65535) * 3.3 * VOLTAGE_DIVIDER_RATIO # Convert the ADC reading to a voltage value
        print(voltage)

        next_update_time = time.ticks_add(current_time, update_delay_ms)
```

`segment_display.py`
```python
from machine import Pin
import time

DIGITS = [
    # .GFEDCBA
    0b00111111, # 0
    0b00000110, # 1
    0b01011011, # 2
    0b01001111, # 3
    0b01100110, # 4
    0b01101101, # 5
    0b01111101, # 6
    0b00000111, # 7
    0b01111111, # 8
    0b01101111, # 9
]

class Display():
    digit_pins = []
    segment_pins = []
    digit_time_on_us = 500
    digit_time_off_us = 100
    
    def __init__(self, DIGIT_1_PIN, DIGIT_2_PIN, DIGIT_3_PIN, DIGIT_4_PIN, SEGMENT_A_PIN, SEGMENT_B_PIN, SEGMENT_C_PIN, SEGMENT_D_PIN, SEGMENT_E_PIN, SEGMENT_F_PIN, SEGMENT_G_PIN, SEGMENT_DP_PIN):
        self.digit_pins = [
            Pin(DIGIT_1_PIN, Pin.OUT),
            Pin(DIGIT_2_PIN, Pin.OUT),
            Pin(DIGIT_3_PIN, Pin.OUT),
            Pin(DIGIT_4_PIN, Pin.OUT),
        ]

        self.segment_pins = [
            Pin(SEGMENT_A_PIN, Pin.OUT),
            Pin(SEGMENT_B_PIN, Pin.OUT),
            Pin(SEGMENT_C_PIN, Pin.OUT),
            Pin(SEGMENT_D_PIN, Pin.OUT),
            Pin(SEGMENT_E_PIN, Pin.OUT),
            Pin(SEGMENT_F_PIN, Pin.OUT),
            Pin(SEGMENT_G_PIN, Pin.OUT),
            Pin(SEGMENT_DP_PIN, Pin.OUT),
        ]
        
    def write_value(self, value, dp=-1):
        # Convert the value to an integer and clamp it to the range 0-9999
        value = max(0, min(9999, value))
        value = int(value)

        for digit_index in range(4):
            dp_enable = (dp == digit_index)
            digit_value = (value // (10 ** (3 - digit_index))) % 10
            self.set_digit(digit_index, digit_value, dp=dp_enable)

    def set_digit(self, digit_index, digit_value, dp=False):
        # Set the common cathode
        for index in range(len(self.digit_pins)):
            digit_on = index == digit_index
            self.digit_pins[index].value(digit_on)

        # Set the segments for the digit
        for index in range(len(self.segment_pins)):
            segment_on = (DIGITS[digit_value] >> index) & 1
            self.segment_pins[index].value(segment_on)
        self.segment_pins[7].value(dp)

        time.sleep_us(self.digit_time_on_us)

        # Turn off all digits to reduce ghosting
        for index in range(len(self.segment_pins)):
            self.segment_pins[index].value(0)

        time.sleep_us(self.digit_time_off_us)
```

### Output
![breadboard setup](/7SegmentVoltmeter/output.JPEG)

## RTC and temperature on LCD-display

### Description
This project uses a DS1302 RTC module to get the current date and time, an LM35 temperature sensor to measure the ambient temperature and it displays this information on a 16x2 I2C LCD display.

The code utilizes external libraries for the LCD display and the RTC module. It initializes the modules and then enters its main loop. Here are 3 independent timers for each component so they can update at different intervals without straining the CPU too much

Componets used:
- 1x RPI Pico W
- 1x DS1302 RTC module
- 1x LM35 temperature sensor
- 1x 16x2 I2C LCD display

### Schematic
![schematic](./RTC_temp_LCD/schematic.png)

### Code
`main.py`
```python
from machine import Pin, SoftI2C, I2C, ADC
from machine_i2c_lcd import I2cLcd
import time
import ds1302

# RTC constants
RTC_CLK_PIN = 5
RTC_DAT_PIN = 7
RTC_RST_PIN = 8

# I2C LCD constants
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

LCD_SDA_PIN = 16
LCD_SCL_PIN = 17

# RTC initialization
rtc_module = ds1302.DS1302(Pin(RTC_CLK_PIN), Pin(RTC_DAT_PIN), Pin(RTC_RST_PIN))

# LCD initialization
i2c = I2C(0, scl=Pin(LCD_SCL_PIN), sda=Pin(LCD_SDA_PIN), freq=400000)
devices = i2c.scan()

i2c_addr = None
for d in devices:
    if d in range(0x20, 0x28):  # PCF8574 I2C address range
        print(f"Setting i2c address: {hex(d)}")
        i2c_addr = d
        break

lcd = I2cLcd(i2c, i2c_addr, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.backlight_on()
lcd.hide_cursor()
lcd.clear()

# LM35 initialization
LM35 = ADC(Pin(26)) 

# set the rtc module
#rtc_module.date_time([2026, 3, 8, 7, 19, 50, 0]) # format: [year, month, day, weekday, hour, minute, second]

# Main loop variables
current_time = time.time()
tmp_read_update_interval = 3  # seconds
next_tmp_read_time = current_time # Read temp every 10 seconds

rtc_update_interval = 1  # seconds
next_rtc_update_time = current_time  # Update RTC display every second

lcd_update_interval = 0.5  # seconds
next_lcd_update_time = current_time# Update LCD every second

try:
    while True:
        current_time = time.time()

        # Get data from temp sensor
        if current_time >= next_tmp_read_time:
            LM35raw = LM35.read_u16()
            LM35temp = (LM35raw / 65535) * 3.3 * 100  # Convert to Celsius

            next_tmp_read_time = current_time + tmp_read_update_interval 

        # Get data from DS1302 RTC
        if current_time >= next_rtc_update_time:
            date_time = rtc_module.date_time()

            next_rtc_update_time = current_time + rtc_update_interval

        # Debug print
        # if date_time is not None:
        #     print(f"Current Date and Time: {date_time[2]:02d}.{date_time[1]:02d}.{date_time[0]:04d} {date_time[4]:02d}:{date_time[5]:02d}:{date_time[6]:02d}")
        # else:
        #     print("Current Date and Time: unavailable")

        # Display on LCD
        if current_time >= next_lcd_update_time:
            if date_time is not None:
                lcd.move_to(0, 0)
                lcd.putstr(f"{date_time[2]:02d}.{date_time[1]:02d}.  {date_time[4]:02d}:{date_time[5]:02d}:{date_time[6]:02d}")
            
            lcd.move_to(0, 1)
            lcd.putstr(f"Temp: {LM35temp:02.1f}C")

            next_lcd_update_time = current_time + lcd_update_interval

except KeyboardInterrupt:
    print("Exiting program.")
    lcd.backlight_off()
```
#### External libraries used:
- LCD API library: https://github.com/dhylands/python_lcd/blob/master/lcd/lcd_api.py
- Machine I2C LCD library: https://github.com/dhylands/python_lcd/blob/master/lcd/machine_i2c_lcd.py
- ds1302 Real Time Clock library: https://github.com/omarbenhamid/micropython-ds1302-rtc/blob/master/ds1302.py

### Output
![breadboard setup](/RTC_temp_LCD/output.JPEG) 

## Dino cheater (HID)

### Description
the Dino cheater project aims to automate the Chrome Dino game using a raspberry to emulate keyboard inputs. To achieve this the contraption has 2 photoresistors that read the screen brightness which can tell the microcontroller if there is an obstacle approaching. I also included a push button that can be used to enable or disable the cheater without having to unplug the device. Achieving a consistent performance with this setup can be quite tricky and might give you varying results based on your displays brightness refresh rate or even ambient light. 

To achieve this in the code i implemented a calibration method which runs initially before the main loop. It takes multiple readings of the photoresistors and based on the highest and lowest observed values it can determine roughly where is the threshold between the background and the obstacles. During the calibration you are expected to expose both photoresistors to the background and the obstacles so it can get a good range of values to work with. After the calibration is done the code enters the main loop where it continuously reads the photoresistors and sends a jump/duck key if it detects an obstacle. To further improve consistency the code also has a short buffer of readings so it doesn't send missinputs in case of a sudden spike. I recommend to keep this buffer short because it can slow reaction time or miss obstacles completely if they don't contribute to the average enough. 

Components used:
- 1x RPI Pico W
- 2x photoresistor
- 2x 220Ω resistor
- 1x 10KΩ resistor
- 1x push button

### Schematic
![schematic](./DinoCheater/schematic.png)

### Code
`main.py`
```python
# Circuit python
import time
import board
import analogio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

BUTTON_PIN = board.GP15
BUILTIN_LED_PIN = board.LED
TOP_PHOTORESISTOR_PIN = board.GP27
BOT_PHOTORESISTOR_PIN = board.GP28

# TOP_BLACK_TRESHHOLD = 2000
# BOT_BLACK_TRESHHOLD = 3000

SENSOR_HISTORY_SIZE = 5
CALIBRATION_SAMPLES = 500
CALIBRATION_SAMPLE_DELAY = 0.01
BLACK_THRESHOLD_FACTOR = 0.35 # 0-1, more = sooner trigger

JUMP_KEY = Keycode.UP_ARROW
DUCK_KEY = Keycode.DOWN_ARROW

# Initialize the devices
button_pin = digitalio.DigitalInOut(BUTTON_PIN)
button_pin.direction = digitalio.Direction.INPUT

built_in_led = digitalio.DigitalInOut(BUILTIN_LED_PIN)
built_in_led.direction = digitalio.Direction.OUTPUT

top_photoresistor = analogio.AnalogIn(TOP_PHOTORESISTOR_PIN)
bot_photoresistor = analogio.AnalogIn(BOT_PHOTORESISTOR_PIN)   

# Initialize the keyboard
kbd = Keyboard(usb_hid.devices)

game_started = False
built_in_led.value = False

top_sensor_history = []
bot_sensor_history = []


def calibrate_photoresistors(sample_count=CALIBRATION_SAMPLES, sample_delay=CALIBRATION_SAMPLE_DELAY):
    top_max = 0
    top_min = 65535
    bot_max = 0
    bot_min = 65535

    print("Calibrating sensors...")
    built_in_led.value = True
    for _ in range(sample_count):
        if(top_photoresistor.value > top_max):
            top_max = top_photoresistor.value
        if(top_photoresistor.value < top_min):
            top_min = top_photoresistor.value
        if(bot_photoresistor.value > bot_max):
            bot_max = bot_photoresistor.value
        if(bot_photoresistor.value < bot_min):
            bot_min = bot_photoresistor.value
        time.sleep(sample_delay)
    built_in_led.value = False

    top_diff = top_max - top_min
    bot_diff = bot_max - bot_min

    top_threshold = top_min + (top_diff * BLACK_THRESHOLD_FACTOR)
    bot_threshold = bot_min + (bot_diff * BLACK_THRESHOLD_FACTOR)

    return top_threshold, bot_threshold


TOP_BLACK_TRESHHOLD, BOT_BLACK_TRESHHOLD = calibrate_photoresistors()

while True:
    top_value = top_photoresistor.value
    bot_value = bot_photoresistor.value

    top_sensor_history.append(top_value)
    if len(top_sensor_history) > SENSOR_HISTORY_SIZE:
        top_sensor_history.pop(0)

    bot_sensor_history.append(bot_value)
    if len(bot_sensor_history) > SENSOR_HISTORY_SIZE:
        bot_sensor_history.pop(0)
    
    top_average = sum(top_sensor_history) / len(top_sensor_history)
    bot_average = sum(bot_sensor_history) / len(bot_sensor_history)

    print(f"Top AVG: {top_average} Bot AVG: {bot_average}  | Top_tresh: {TOP_BLACK_TRESHHOLD} Bot_tresh: {BOT_BLACK_TRESHHOLD}") 

    button_value = bool(button_pin.value)
    if(button_value):
        print("Starting game")
        game_started = not game_started
        built_in_led.value = game_started
        if game_started:
            kbd.press(JUMP_KEY)
            kbd.release(JUMP_KEY)
            kbd.press(DUCK_KEY)
            kbd.release(DUCK_KEY)
        else:
            kbd.release(JUMP_KEY)
            kbd.release(DUCK_KEY)
        time.sleep(1)

    if(game_started):
        # Avoid cactus
        if(bot_average < BOT_BLACK_TRESHHOLD):
            print("Jump")
            kbd.press(JUMP_KEY)
            built_in_led.value = False
            time.sleep(0.25)
            kbd.release(JUMP_KEY)
            kbd.press(DUCK_KEY)
            time.sleep(0.075)
            kbd.release(DUCK_KEY)
            built_in_led.value = True
        
        # Avoid flying bird
        if(top_average < TOP_BLACK_TRESHHOLD and bot_average > BOT_BLACK_TRESHHOLD):
            print("Duck")
            kbd.press(DUCK_KEY)
            built_in_led.value = False
            time.sleep(0.6)
            kbd.release(DUCK_KEY)
            built_in_led.value = True
```

#### External libraries used:
- Adafruit HID keyboard library: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keyboard.py
- Adafruit HID keycode library: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keycode.py

### Output
![breadboard setup](./DinoCheater/output.JPEG)

## Analog joystick (HID)

### Description
This project makes the Rpi pico act as a HID keyboard that is controlled by a 2-axis analog joystick and a push button. This setup can be used to play simple games like tertis or super mario bros by mapping the joystick movements to the arrow keys. 

The code relies on the Adafruit HID library to send keyboard inputs to the PC. It reads the values from the joystick and the button and based on that it sends the corresponding key presses. The joystick has a deadzone to prevent random missinputs when the joystick is near the center position. 

Components used:
- 1x RPI Pico W
- 1x 2-axis analog joystick
- 1x 10kΩ resistor
- 1x push button

### Schematic
![schematic](./AnalogJoystick/schematic.png)

### Code
`main.py`
```python
import time
import board
import analogio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

JOYSTICK_DEADZONE_PERCENT = 10  # Deadzone for joystick input. Goes both ways so 5$ means from 45 to 55 is deadzone

# Define the pins for the input devices
x_pin = analogio.AnalogIn(board.GP26)  # A0
y_pin = analogio.AnalogIn(board.GP27)  # A1

button_pin = digitalio.DigitalInOut(board.GP15)
button_pin.direction = digitalio.Direction.INPUT

# Init keyboard object for sending input to PC
kbd = Keyboard(usb_hid.devices)

button_pressed = False
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False

while True:
    # Read the input values
    x_value = (x_pin.value / 65535) * 100  # Scale to 0-100
    y_value = (y_pin.value / 65535) * 100  # Scale to 0-100
    button_value = bool(button_pin.value)

    # Print the joystick values for debug
    # print("X: {:.2f} Y:{:.2f} Button: {}".format(x_value, y_value, button_value))

    #determine actions
    move_left = x_value < (50 - JOYSTICK_DEADZONE_PERCENT)
    move_right = x_value > (50 + JOYSTICK_DEADZONE_PERCENT)
    move_up = y_value < (50 - JOYSTICK_DEADZONE_PERCENT)
    move_down = y_value > (50 + JOYSTICK_DEADZONE_PERCENT)
    
    if(button_value != button_pressed):
        button_pressed = button_value
        if button_pressed:
            kbd.press(Keycode.SPACE)
        else:
            kbd.release(Keycode.SPACE)

    # Joystick movement x-axis
    if move_left != left_pressed:
        left_pressed = move_left
        if left_pressed:
            kbd.press(Keycode.LEFT_ARROW)
        else:
            kbd.release(Keycode.LEFT_ARROW)

    if move_right != right_pressed:
        right_pressed = move_right
        if right_pressed:
            kbd.press(Keycode.RIGHT_ARROW)
        else:
            kbd.release(Keycode.RIGHT_ARROW)

    # Joystick movement y-axis
    if move_up != up_pressed:
        up_pressed = move_up
        if up_pressed:
            kbd.press(Keycode.UP_ARROW)
        else:
            kbd.release(Keycode.UP_ARROW)

    if move_down != down_pressed:
        down_pressed = move_down
        if down_pressed:
            kbd.press(Keycode.DOWN_ARROW)
        else:
            kbd.release(Keycode.DOWN_ARROW)

    time.sleep(0.01)  # Small delay to prevent excessive CPU usage
```

#### External libraries used:
- Adafruit HID keyboard library: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keyboard.py
- Adafruit HID keycode library: https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keycode.py

### Output
![breadboard setup](./AnalogJoystick/output.JPEG)

## WiFi scanner

### Description
This project utilizes the WiFi capabilities of the RPI Pico W to scan for nearby WiFi access points and display them on a web interface. 

The pico first connects to a WiFi network using the credentials provided in the `secrets.py` file so it can serve the web interface. If you are recreating this project you need to create your own `secrets.py` file based on the `secrets.py.example` file with your own credentials. The web server listens for incoming HTTP requests and serves the `index.html` page when the root end point is called. The page itself that periodically makes requests to the `/scan` endpoint back from the pico. Calling this endpoint triggers a WiFi scan on the pico which returns a list of nearby WiFi networks sorted by signal strength. The web page then displays this list in a table format.

Components used:
- 1x RPI Pico W

### Schematic
Not applicable for this project - its only the standalone pico w

### Code
`main.py`
```python
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
```

`secrets.py.example`
```python
# WiFi credentials 
SSID = "YOUR_NET_SSID"
PASSWORD = "YOUR_NET_PASS"
```

`index.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Scanner</title>
    <style>
      table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
      }
    </style>
</head>
<body>
  <h1>Available WiFi Networks</h1>
  <table>
    <thead>
      <tr><th>Nr</th><th>SSID</th><th>RSSI</th></tr>
    </thead>
    <tbody id="rows"></tbody>
  </table>

  <script>
    async function refreshScan() {
      const rows = document.getElementById('rows');

      try {
        const response = await fetch('/scan');
        const data = await response.json();

        if (!data.ok) {
            return;
        }
        
        rows.innerHTML = '';

        ac_points = data.networks
        for (let i = 0; i < ac_points.length; i++) {
            const ap = ac_points[i];
            const row = document.createElement('tr');
            row.innerHTML = `<td>${ap.nr}</td><td>${ap.ssid}</td><td>${ap.rssi} dBm</td>`;
            rows.appendChild(row);
        }

      } catch (err) {
            return;
        }
    }

    refreshScan();
    setInterval(refreshScan, 10000);
  </script>
</body>
</html>
```

### Output
![breadboard setup](./WiFiScanner/output.png)

## Controlling stuff (Webserver)

### Description

### Code
```python

```

### Schematic
![schematic](./ControllingStuff/schematic.png)

### Output
![breadboard setup](./ControllingStuff/output.JPEG)
![web interface](./ControllingStuff/output2.png)

## Attendance (RFID, RTC, web and LCD)

### Description

### Code
```python

```

### Schematic
![schematic](./Attendance/schematic.png)

### Output
![breadboard setup](./Attendance/output.JPEG)
![web interface](./Attendance/output2.png)
