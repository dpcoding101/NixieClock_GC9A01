import time
import random  # Add this import
from machine import Pin, SPI
import gc9a01
import vga1_16x16  # Font module

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

# 📌 Initialize SPI interface (shared)
spi = SPI(0, baudrate=40000000, polarity=0, phase=0, sck=Pin(TFT_SCK), mosi=Pin(TFT_MOSI))

# 📌 Initialize the displays
displays = [
    gc9a01.GC9A01(spi, cs=Pin(TFT1_CS), dc=Pin(TFT1_DC), reset=Pin(TFT1_RES), rotation=0),
    gc9a01.GC9A01(spi, cs=Pin(TFT2_CS), dc=Pin(TFT2_DC), reset=Pin(TFT2_RES), rotation=0),
    gc9a01.GC9A01(spi, cs=Pin(TFT3_CS), dc=Pin(TFT3_DC), reset=Pin(TFT3_RES), rotation=0),
    gc9a01.GC9A01(spi, cs=Pin(TFT4_CS), dc=Pin(TFT4_DC), reset=Pin(TFT4_RES), rotation=0)
]

# 📌 Binary animation function
def draw_binary_screen():
    for _ in range(2):  # Run animation for a few seconds
        for tft in displays:
            tft.fill(0)  # Clear the display
            for row in range(0, tft.height, 16):  # Step by font height
                for col in range(0, tft.width, 16):  # Step by font width
                    binary_number = str(random.randint(0, 1))  # Generate random 0 or 1
                    tft.text(vga1_16x16, binary_number, col, row, gc9a01.color565(0, 255, 0))  # Green text
        time.sleep(0.5)  # Short delay before refreshing

# 📌 Function to start binary loading screen
def run():
    draw_binary_screen()
    time.sleep(1)  # Short delay before switching to the clock
    import clock  # Switch to clock.py

# Only run automatically if executed directly
if __name__ == "__main__":
    run()
