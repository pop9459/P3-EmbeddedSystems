# Micropython code
from rgb_led import RgbLed
from machine import Pin, I2C
import time
import ds1302
import buzzer
import machine_i2c_lcd
from mfrc522 import MFRC522
from attendance_db import AttendanceDB

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
buzzer = buzzer.Buzzer(Pin(BUZZER_PIN))

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

while True:
	# RGB led example
	# rgb_led.set_color(True, False, False) # Red
	# time.sleep(0.5)
	# rgb_led.set_color(False, True, False) # Green
	# time.sleep(0.5)
    # rgb_led.set_color(False, False, True) # Blue
    # time.sleep(0.5)

    # RTC example
	now = rtc.date_time()
	if now is None:
		time.sleep(1)
		continue
	y, m, d, w, hh, mm, ss = now
	print("{:04d}-{:02d}-{:02d} ({}) {:02d}:{:02d}:{:02d}".format(y, m, d, w, hh, mm, ss))
	time.sleep(1)
	
	# LCD example
	# now = rtc.date_time()
	# lcd.clear()
	# lcd.move_to(0, 0)
	# lcd.putstr("I2C: 0x{:02X}".format(lcd_addr))
	# if now is not None:
	# 	y, m, d, w, hh, mm, ss = now
	# 	lcd.move_to(0, 1)
	# 	lcd.putstr("{:02d}:{:02d}:{:02d}".format(hh, mm, ss))
	# else:
	# 	lcd.move_to(0, 1)
	# 	lcd.putstr("No RTC data")
	# time.sleep(1)

	# RFID reader example
	# stat, bits = rfid.request(rfid.REQIDL)
	# if stat == rfid.OK:
	# 	stat, uid = rfid.SelectTagSN()
	# 	if stat == rfid.OK:
	# 		print("Card detected! UID: {}".format([hex(b) for b in uid]))
	# 		rgb_led.set_color(False, True, False)  # Green for success
	# 		time.sleep(0.5)
	# 		rgb_led.set_color(False, False, False)  # Off
	# 	else:
	# 		print("Could not read card UID")




	pass