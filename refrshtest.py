import time
from machine import Pin, SPI
import gc9a01
from fonts.romfonts import vga2_bold_16x32 as font

# Pin Configuration
TFT_SCK = 18  
TFT_MOSI = 19  

# Display 1 (Hours Tens)
TFT1_CS = 22
TFT1_DC = 21
TFT1_RES = 20

# Display 2 (Hours Ones)
TFT2_CS = 28
TFT2_DC = 29
TFT2_RES = 17

# Display 3 (Minutes Tens)
TFT3_CS = 5
TFT3_DC = 4
TFT3_RES = 3

# Display 4 (Minutes Ones)
TFT4_CS = 15
TFT4_DC = 14
TFT4_RES = 13

# Initialize SPI (shared for all displays)
spi = SPI(0, baudrate=60000000, sck=Pin(TFT_SCK), mosi=Pin(TFT_MOSI))

# Initialize displays
displays = [
    gc9a01.GC9A01(spi, dc=Pin(TFT1_DC, Pin.OUT), cs=Pin(TFT1_CS, Pin.OUT), reset=Pin(TFT1_RES, Pin.OUT), rotation=0),
    gc9a01.GC9A01(spi, dc=Pin(TFT2_DC, Pin.OUT), cs=Pin(TFT2_CS, Pin.OUT), reset=Pin(TFT2_RES, Pin.OUT), rotation=0),
    gc9a01.GC9A01(spi, dc=Pin(TFT3_DC, Pin.OUT), cs=Pin(TFT3_CS, Pin.OUT), reset=Pin(TFT3_RES, Pin.OUT), rotation=0),
    gc9a01.GC9A01(spi, dc=Pin(TFT4_DC, Pin.OUT), cs=Pin(TFT4_CS, Pin.OUT), reset=Pin(TFT4_RES, Pin.OUT), rotation=0)
]

# Function to clear all displays
def clear_displays():
    for display in displays:
        display.fill(0)  # Fill with black (clear)
        time.sleep(0.1)  # Short delay between updates

# Function to test refreshing by showing numbers on all displays
def test_refresh():
    for i in range(10):  # Cycle numbers 0-9
        for idx, display in enumerate(displays):
            display.fill(0)  # Clear screen
            text = str(i)  # Convert number to string
            col = (display.width - font.WIDTH) // 2  # Center horizontally
            row = (display.height - font.HEIGHT) // 2  # Center vertically
            display.text(font, text, col, row, gc9a01.color565(255, 255, 255))  # White text
        time.sleep(0.5)  # Delay to observe changes

# Function to test different colors
def test_colors():
    colors = [
        gc9a01.color565(255, 0, 0),   # Red
        gc9a01.color565(0, 255, 0),   # Green
        gc9a01.color565(0, 0, 255),   # Blue
        gc9a01.color565(255, 255, 0), # Yellow
        gc9a01.color565(255, 255, 255) # White
    ]
    
    for color in colors:
        for display in displays:
            display.fill(color)  # Fill with color
        time.sleep(0.5)  # Delay to observe changes

# Main test function
def main():
    clear_displays()
    test_colors()
    test_refresh()
    clear_displays()

# Run the test
main()
