from machine import Pin
import time

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        self.pin.init(Pin.OUT)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def beep(self, duration=0.1):
        self.on()
        time.sleep(duration)
        self.off()

    def play_tone(self, frequency, duration):
        period = 1 / frequency
        cycles = int(frequency * duration)
        for _ in range(cycles):
            self.on()
            time.sleep(period / 2)
            self.off()
            time.sleep(period / 2)

    def play_rising_tone(self):
        self.play_tone(110, 0.2)
        self.play_tone(130, 0.2)
        self.play_tone(180, 0.2)

    def play_falling_tone(self):
        self.play_tone(180, 0.2) # A4 note for 2 seconds
        self.play_tone(130, 0.2) # A4 note for 2 seconds
        self.play_tone(110, 0.2) # A4 note for 2 seconds