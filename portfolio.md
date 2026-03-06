# Digital portfolio Embedded systems Y1 P3
Name: Peter Kapsiar
Student ID: 5486866

## Blink with hardware reset
### Code
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

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/IMG_5917.JPEG)

## Mario pico

### Code
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

### Description

### Output
![console output](/MarioPico/image.png)

## 7-Segments Voltmeter (0..10V)

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)

## RTC and temperature on LCD-display

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)

## Dino cheater (HID)

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)

## Analog joystick (HID)

### Code
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

### Description

### Output
![breadboard setup](/AnalogJoystick/IMG_5918.JPEG)

## WiFi scanner

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)

## Controlling stuff (Webserver)

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)

## Attendance (RFID, RTC, web and LCD)

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)

## Solo pico project (not mandatory) 

### Code
```python

```

### Description

### Output
![breadboard setup](./BlinkWithExternalHardwareReset/image.jpg)
