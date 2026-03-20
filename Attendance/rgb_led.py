from machine import Pin

class RgbLed:
    def __init__(self, r_pin, g_pin, b_pin):
        self.r = Pin(r_pin, Pin.OUT)
        self.g = Pin(g_pin, Pin.OUT)
        self.b = Pin(b_pin, Pin.OUT)

    def set_color(self, r: bool, g: bool, b: bool):
        self.r.value(r)
        self.g.value(g)
        self.b.value(b)
