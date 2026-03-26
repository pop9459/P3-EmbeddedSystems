# Micropython code

from rgb_led import RgbLed
from machine import Pin, I2C
import ds1302
import buzzer as Buzzer
import machine_i2c_lcd
from mfrc522 import MFRC522
from attendance_db import AttendanceDB
from web_server import connect_wifi, send_json, serve_file
import socket
import time
import json

# Pin definitions
BUZZER_PIN = 2
RTC_RST_PIN = 5
RTC_DAT_PIN = 6
RTC_CLK_PIN = 7
LCD_SDA_PIN = 8
LCD_SCL_PIN = 9
RFID_READER_SDA_PIN = 14
RFID_READER_SCK_PIN = 10
RFID_READER_MOSI_PIN = 11
RFID_READER_MISO_PIN = 12
RFID_READER_RST_PIN = 17
LED_B_PIN = 18
LED_G_PIN = 19
LED_R_PIN = 20

SET_RTC_ON_BOOT = False
REGISTER_TIME_WINDOW_SECONDS = 30
RFID_POLL_INTERVAL_MILLIS = 100
TIME_UPDATE_INTERVAL_MILLIS = 250
LCD_UPDATE_INTERVAL_MILLIS = 250

# Initialize peripherals
# RGB LED initialization
rgb_led = RgbLed(LED_R_PIN, LED_G_PIN, LED_B_PIN)

# RTC initialization
rtc = ds1302.DS1302(
	Pin(RTC_CLK_PIN),
	Pin(RTC_DAT_PIN),
	Pin(RTC_RST_PIN)
)

if SET_RTC_ON_BOOT:
	rtc.date_time([2026, 3, 20, 5, 19, 6, 0])
	rtc.start()

# Buzzer initialization
buzzer = Buzzer.Buzzer(Pin(BUZZER_PIN))

# LCD initialization
i2c = I2C(0, sda=Pin(LCD_SDA_PIN), scl=Pin(LCD_SCL_PIN), freq=400000)
devices = i2c.scan()
lcd_addr = machine_i2c_lcd.DEFAULT_I2C_ADDR
if devices and lcd_addr not in devices:
	lcd_addr = devices[0]

lcd = machine_i2c_lcd.I2cLcd(i2c, lcd_addr, 2, 16)
lcd.clear()
lcd.putstr("LCD ready")

# RFID reader initialization
rfid = MFRC522(
	sck=Pin(RFID_READER_SCK_PIN),
	mosi=Pin(RFID_READER_MOSI_PIN),
	miso=Pin(RFID_READER_MISO_PIN),
	rst=Pin(RFID_READER_RST_PIN),
	cs=Pin(RFID_READER_SDA_PIN),
	spi_id=1
)

# Attendance database initialization
attendance_db = AttendanceDB()

# Configure WiFi and start web server
connect_wifi()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.settimeout(0.2) # Important - socket will block execution otherwise


# Helper functions
def uid_to_key(uid):
	"""Convert UID list/bytes/string into a stable dict key."""
	if isinstance(uid, (list, tuple)):
		# Example: [4, 163, 27, 44] -> "04A31B2C"
		return ''.join('{:02X}'.format(x) for x in uid)
	return str(uid)


def readRfidCard():
	"""Read an RFID card and return its UID as a string key, or None if no card is present."""
	stat, bits = rfid.request(rfid.REQIDL)
	if stat == rfid.OK:
		stat, uid = rfid.SelectTagSN()
		if stat == rfid.OK:
			return uid_to_key(uid)
	return None

def readRfidCardForTime(time_window_seconds):
	"""Attempt to read an RFID card for a specified time window."""
	start_time = time.time()
	while time.time() - start_time < time_window_seconds:
		uid = readRfidCard()
		if uid is not None:
			return uid
		time.sleep_ms(RFID_POLL_INTERVAL_MILLIS)
			
	# No card detected within the time window
	return None


def registerCard(name): 
	"""Register a new card to the database with the given name. Returns True on success, False on failure."""
	rgb_led.set_color(False, False, True)  # Blue for registration mode
	if name is None or name.strip() == "":
		rgb_led.blink_color(True, False, False)  # Red for error
		return False
	
	name = name.strip() 
	uid = readRfidCardForTime(REGISTER_TIME_WINDOW_SECONDS)
	
	if uid is  None:
		rgb_led.blink_color(True, False, False)  # Red for error
		return False
	
	attendance_db.register_card(uid=uid, name=name)
	
	rgb_led.blink_color(False, True, False)  # Green for success
	return True


def checkIn(uid, timestamp):
	"""Check in or out a card with the given UID and timestamp. Returns (success, message)."""
	success, message = attendance_db.check_in(uid, timestamp)
	if success:
		name = attendance_db.load_json_file(attendance_db.known_cards_filename).get(uid, "Unknown")
		if(message == "Checked in"):
			rgb_led.set_color(False, True, False)  # Green for success
			write_to_lcd("Welcome", line=0)
			write_to_lcd("{}".format(name), line=1)
			buzzer.play_rising_tone()
			rgb_led.off()
		elif(message == "Checked out"):
			rgb_led.set_color(True, True, False)  # Yellow for check-out
			write_to_lcd("Goodbye", line=0)
			write_to_lcd("{}".format(name), line=1)
			buzzer.play_falling_tone()
			rgb_led.off()
	else:
		if message == "Card not registered":
			rgb_led.set_color(True, False, False)
			write_to_lcd("Unknown card", line=0)
			buzzer.play_error_tone()
			rgb_led.off()
		elif message == "Already checked in and out for today":
			rgb_led.set_color(True, False, False)  # Red for already checked in/out
			write_to_lcd("Already out", line=0)
			buzzer.play_error_tone()
			rgb_led.off()
	
	time.sleep(2)  # Keep message on LCD for a moment before clearing
	return success, message


def write_to_lcd(message, line=0):
	"""Helper function to write a message to the LCD on a specific line (0 or 1)."""
	lcd.move_to(0, line)
	text = str(message)
	if len(text) < 16:
		text = text + (" " * (16 - len(text)))
	else:
		text = text[:16]
	lcd.putstr(text)


# Main loop setup
next_time_update = time.ticks_ms() + TIME_UPDATE_INTERVAL_MILLIS
next_lcd_update = time.ticks_ms() + LCD_UPDATE_INTERVAL_MILLIS
next_rfid_read = time.ticks_ms() + RFID_POLL_INTERVAL_MILLIS
now = None

# Main loop
while True:
	# Update time from RTC
	if time.ticks_ms() >= next_time_update:
		now = rtc.date_time()
		next_time_update = time.ticks_ms() + TIME_UPDATE_INTERVAL_MILLIS
	
	# Update LCD with current info
	if time.ticks_ms() >= next_lcd_update:
		write_to_lcd("Please scan card", line=0)

		if now is not None:
			y, m, d, w, hh, mm, ss = now
			write_to_lcd("{:02d}:{:02d}:{:02d} | {:02d}.{:02d}".format(hh, mm, ss, d, m), line=1)	
		else:
			write_to_lcd("No RTC data", line=1)

		next_lcd_update = time.ticks_ms() + LCD_UPDATE_INTERVAL_MILLIS

	# Read RFID card and check in/out
	if time.ticks_ms() >= next_rfid_read:
		uid = readRfidCard()
		if uid is not None and now is not None:
			success, message = checkIn(uid, now)
			print("Card UID: {}, Result: {}, Message: {}".format(uid, success, message))
		
		next_rfid_read = time.ticks_ms() + RFID_POLL_INTERVAL_MILLIS

	# Handle web server requests without blocking periodic tasks.
	try:
		conn, addr = s.accept()
	except OSError:
		conn = None

	if conn is not None:
		try:
			request = conn.recv(1024).decode()
			header_end = request.find('\r\n\r\n')
			body = request[header_end + 4:].strip() if header_end != -1 else ""
			json_payload = json.loads(body) if body else {}

			# server index.html for root route
			if 'GET / ' in request:
				serve_file(conn, 'index.html')
			
			# Get attendance records route
			elif 'GET /attendanceRecords' in request:
				todays_records = attendance_db.get_attendance_records_by_day(now)
				send_json(conn, '200 OK', todays_records)

			# New card registration request route
			elif 'POST /registerCard' in request:
				name = json_payload.get('name')
				if name is None or name.strip() == "":
					send_json(conn, '400 Bad Request', {
						'error': 'Name is required to register a card',
					})
				elif registerCard(name):
					send_json(conn, '200 OK', {
						'message': 'Card registered successfully',
					})
				else:
					send_json(conn, '400 Bad Request', {
						'error': 'Failed to register card',
					})
			
			# Registered cards retrieval route
			elif 'GET /registeredCards' in request:
				known_cards = attendance_db.load_json_file(attendance_db.known_cards_filename)
				send_json(conn, '200 OK', known_cards)
			
			elif 'POST /clearDatabase' in request:
				attendance_db.clear_db()
				send_json(conn, '200 OK', {
					'message': 'Database cleared successfully',
				})
				rgb_led.blink_color(True, True, True, delay_ms=1000)  # White blink to indicate DB cleared

			else:
				send_json(conn, '404 Not Found', {
					'error': 'Route not found',
				})
		except Exception:
			pass
		finally:
			conn.close()
