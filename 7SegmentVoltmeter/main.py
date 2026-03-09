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