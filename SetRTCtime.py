from machine import Pin, I2C
from ds1307 import DS1307
import time

# Initialize I2C with your specified pins
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Make sure these pins are correct

# Initialize DS1307 RTC
rtc = DS1307(i2c)

# Set the time once if necessary
try:
    rtc.set_time(hours=16, minutes=21, seconds=0)  # Example time: 12:00:00
    print("Time has been set.")
except Exception as e:
    print("Error setting RTC time:", e)

# Fetch and print the current time
try:
    current_time = rtc.get_time()
    print("RTC Time:", current_time)
except Exception as e:
    print("Error reading RTC:", e)
