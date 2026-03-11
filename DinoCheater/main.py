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
LEFT_PHOTORESISTOR_PIN = board.GP27
RIGHT_PHOTORESISTOR_PIN = board.GP28

BLACK_TRESHHOLD = 3500

JUMP_KEY = Keycode.UP_ARROW

# Initialize the devices
button_pin = digitalio.DigitalInOut(BUTTON_PIN)
button_pin.direction = digitalio.Direction.INPUT

built_in_led = digitalio.DigitalInOut(BUILTIN_LED_PIN)
built_in_led.direction = digitalio.Direction.OUTPUT

left_photoresistor = analogio.AnalogIn(LEFT_PHOTORESISTOR_PIN)
right_photoresistor = analogio.AnalogIn(RIGHT_PHOTORESISTOR_PIN)   

# Initialize the keyboard
kbd = Keyboard(usb_hid.devices)

game_started = False
built_in_led.value = False

while True:
    button_value = bool(button_pin.value)
    if(button_value):
        print("Starting game")
        game_started = not game_started
        built_in_led.value = game_started
        time.sleep(1)
        if game_started:
            kbd.press(JUMP_KEY)

    if(game_started):
        left_value = left_photoresistor.value
        right_value = right_photoresistor.value

        print("Left: {} Right: {}".format(left_value, right_value))

        if(left_value < BLACK_TRESHHOLD):
            time.sleep(0.2)
            kbd.press(JUMP_KEY)
            time.sleep(0.2)
            kbd.release(JUMP_KEY)
            print("Jump")
            time.sleep(0.5)
