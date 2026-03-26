from machine import Pin
import time

class RgbLed:
    def __init__(self, r_pin, g_pin, b_pin):
        self.r = Pin(r_pin, Pin.OUT)
        self.g = Pin(g_pin, Pin.OUT)
        self.b = Pin(b_pin, Pin.OUT)

    def off(self):
        self.set_color(False, False, False)

    def set_color(self, r: bool, g: bool, b: bool):
        self.r.value(r)
        self.g.value(g)
        self.b.value(b)

    def blink_color(self, r: bool, g: bool, b: bool, delay_ms=500):
        self.set_color(r, g, b)
        time.sleep_ms(delay_ms)
        self.set_color(False, False, False)  # Off