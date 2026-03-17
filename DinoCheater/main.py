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