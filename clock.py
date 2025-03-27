import time
from machine import Pin, SPI, I2C
import gc9a01
from ds1307 import DS1307
import vga1_16x16  # Import the VGA font (make sure the file is present)


# 📌 Turn off the onboard red LED (GPIO 25)
led = Pin(25, Pin.OUT)
led.value(1)  # Set the LED to low (turn off)
#led.value(1)  # Set the LED to high (turn on)


# 📌 Pin assignments for all four displays
TFT_SCK = 18
TFT_MOSI = 19

# Display 1 (Hours Tens)
TFT1_CS = 22
TFT1_DC = 29
TFT1_RES = 28

# Display 2 (Hours Ones)
TFT2_CS = 20
TFT2_DC = 21
TFT2_RES = 17

# Display 3 (Minutes Tens)
TFT3_CS = 5
TFT3_DC = 4
TFT3_RES = 3

# Display 4 (Minutes Ones)
TFT4_CS = 15
TFT4_DC = 14
TFT4_RES = 13

# RTC pins (SCL, SDA)
I2C_SCL = 1  
I2C_SDA = 0  

# 📌 Initialize SPI interface (shared)
spi = SPI(0, baudrate=40000000, polarity=0, phase=0, sck=Pin(TFT_SCK), mosi=Pin(TFT_MOSI))

# 📌 Initialize the displays
displays = [
    gc9a01.GC9A01(spi, cs=Pin(TFT1_CS), dc=Pin(TFT1_DC), reset=Pin(TFT1_RES), rotation=0),
    gc9a01.GC9A01(spi, cs=Pin(TFT2_CS), dc=Pin(TFT2_DC), reset=Pin(TFT2_RES), rotation=0),
    gc9a01.GC9A01(spi, cs=Pin(TFT3_CS), dc=Pin(TFT3_DC), reset=Pin(TFT3_RES), rotation=0),
    gc9a01.GC9A01(spi, cs=Pin(TFT4_CS), dc=Pin(TFT4_DC), reset=Pin(TFT4_RES), rotation=0)
]

# 📌 Initialize I2C for DS1307 RTC
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
rtc = DS1307(i2c)

# 📌 Initialize buttons for adjusting time
set_time_button = Pin(8, Pin.IN, Pin.PULL_UP)  # Button to set time mode (Pin 8)
increase_button = Pin(6, Pin.IN, Pin.PULL_UP)  # Button to increase time (Pin 6)
decrease_button = Pin(7, Pin.IN, Pin.PULL_UP)  # Button to decrease time (Pin 7)

# 📌 Traditional digit representations (same as your previous code)
traditional_digits = {
    "0": [
        " **** ",
        "*    *",
        "*    *",
        "*    *",
        "*    *",
        "*    *",
        " **** "
    ],
    "1": [
        "  *  ",
        " **  ",
        "  *  ",
        "  *  ",
        "  *  ",
        "  *  ",
        " *** "
    ],
    "2": [
        " **** ",
        "*    *",
        "    * ",
        "   *  ",
        "  *   ",
        " *    ",
        "******"
    ],
    "3": [
        " **** ",
        "*    *",
        "     *",
        "  *** ",
        "     *",
        "*    *",
        " **** "
    ],
    "4": [
        "*   * ",
        "*   * ",
        "*   * ",
        "******",
        "    * ",
        "    * ",
        "    * "
    ],
    "5": [
        "******",
        "*     ",
        "*     ",
        "***** ",
        "     *",
        "*    *",
        " **** "
    ],
    "6": [
        " **** ",
        "*    *",
        "*     ",
        "***** ",
        "*    *",
        "*    *",
        " **** "
    ],
    "7": [
        "******",
        "     *",
        "    * ",
        "   *  ",
        "  *   ",
        " *    ",
        " *    "
    ],
    "8": [
        " **** ",
        "*    *",
        "*    *",
        " **** ",
        "*    *",
        "*    *",
        " **** "
    ],
    "9": [
        " **** ",
        "*    *",
        "*    *",
        " *****",
        "     *",
        "*    *",
        " **** "
    ]
}

def draw_traditional_digit(tft, digit, x_offset, y_offset, scale_x=14, scale_y=16, color=gc9a01.color565(255, 255, 255)):
    """Draws a traditional digit with scaling and color."""
    if digit not in traditional_digits:
        return
    grid = traditional_digits[digit]
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == "*":
                for i in range(scale_x):  # Scale in X direction
                    for j in range(scale_y):  # Scale in Y direction
                        x = x_offset + col_idx * scale_x + i
                        y = y_offset + row_idx * scale_y + j
                        tft.pixel(x, y, color)  # Draw the pixel with the specified color

def show_traditional_number(tft, number, color=gc9a01.color565(255, 255, 255)):
    """Displays a traditional number on screen with a specified color."""
    tft.fill(0)  # Clear screen
    text = str(number)
    num_digits = len(text)
    digit_width = 6 * 14  # Adjust width for the scaled grid (scale=14)
    total_width = num_digits * digit_width
    start_x = (240 - total_width) // 2  # Center horizontally
    start_y = (240 - 7 * 16) // 2  # Center vertically
    for i, digit in enumerate(text):
        draw_traditional_digit(tft, digit, start_x + i * digit_width, start_y, scale_x=14, scale_y=16, color=color)

# 📌 Show number with vga1_16x16 font
def show_vga_number(tft, number):
    """Displays a number using the vga1_16x16 font on the screen."""
    tft.fill(0)  # Clear screen
    text = str(number)
    num_digits = len(text)
    x_offset = (240 - (num_digits * 16)) // 2  # Center horizontally
    y_offset = (240 - 16) // 2  # Center vertically
    for i, digit in enumerate(text):
        # Use the 'print_char' method of the font to draw the character
        vga1_16x16.print_char(tft, x_offset + (i * 16), y_offset, digit, gc9a01.color565(255, 255, 255))


# 📌 Update the display with the current RTC time
def update_display(previous_time):
    # Get the current time from RTC
    hours, minutes, _ = rtc.get_time()  # Ensure we get hours and minutes
    
    # Check if the time has changed
    current_time = (hours, minutes)
    
    # Only proceed if the time has actually changed
    if current_time != previous_time:
        # Format the time as a string
        time_str = f"{hours:02d}:{minutes:02d}"
        
        # Split the time string into individual digits (without colon)
        digits = list(time_str.replace(":", ""))  # Remove colon to get digits as list
        
        # Ensure we are comparing the correct indices
        if digits[3] != previous_time[1] % 10:  # Check if minutes ones digit changed
            show_traditional_number(displays[3], digits[3])  # Update minutes ones display
        if digits[2] != previous_time[1] // 10:  # Check if minutes tens digit changed
            show_traditional_number(displays[2], digits[2])  # Update minutes tens display
        if digits[1] != previous_time[0] % 10:  # Check if hours ones digit changed
            show_traditional_number(displays[1], digits[1])  # Update hours ones display
        if digits[0] != previous_time[0] // 10:  # Check if hours tens digit changed
            show_traditional_number(displays[0], digits[0])  # Update hours tens display

        return current_time  # Return the updated time
    return previous_time  # Return the same time if no change



# 📌 Time adjustment function (optimized to update only the changed display)
def adjust_time():
    # Check if in set time mode
    if set_time_button.value() == 0:  # Button pressed (active low)
      
        
        # Cycle between changing hours and minutes
        mode = 0  # 0 = Change Hours, 1 = Change Minutes
        while True:
            hours, minutes, _ = rtc.get_time()
            
            if mode == 0:  # Change Hours
                while True:
                    # Only update the hours display
                    show_traditional_number(displays[0], hours)  # Hours tens display
                    show_traditional_number(displays[1], hours % 10)  # Hours ones display
                    update_display(previous_time)  # Keep showing the current minutes on other displays

                    if increase_button.value() == 0:  # Increase hours
                        hours += 1
                        if hours == 24:
                            hours = 0
                        rtc.set_time(hours, minutes, 0)
                        break
                    elif decrease_button.value() == 0:  # Decrease hours
                        hours -= 1
                        if hours == -1:
                            hours = 23
                        rtc.set_time(hours, minutes, 0)
                        break
            elif mode == 1:  # Change Minutes
                while True:
                    # Only update the minutes display
                    show_traditional_number(displays[2], minutes // 10)  # Minutes tens display
                    show_traditional_number(displays[3], minutes % 10)  # Minutes ones display
                    update_display(previous_time)  # Keep showing the current hours on other displays
                    
                    if increase_button.value() == 0:  # Increase minutes
                        minutes += 1
                        if minutes == 60:
                            minutes = 0
                            hours += 1
                            if hours == 24:
                                hours = 0
                        rtc.set_time(hours, minutes, 0)
                        break
                    elif decrease_button.value() == 0:  # Decrease minutes
                        minutes -= 1
                        if minutes == -1:
                            minutes = 59
                            hours -= 1
                            if hours == -1:
                                hours = 23
                        rtc.set_time(hours, minutes, 0)
                        break
            mode = (mode + 1) % 2  # Switch mode between hours and minutes
            
            if set_time_button.value() == 0:  # If button pressed again, save and exit
                # Break and save time
                break



# Main loop to update the display only when the time changes and adjust time if needed
previous_time = (0, 0)  # Initialize previous_time to a valid value (e.g., 00:00)
while True:
    previous_time = update_display(previous_time)  # Update display
    adjust_time()  # Check if time adjustment is needed
    time.sleep(1)  # Sleep for 1 second



