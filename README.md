# NixieClock_GC9A01
The following is code for a minimal nixie clock that uses four GC9A01 displays, DS1307 RTC and a Raspberry PICO RP2040.

![20250328_111458](https://github.com/user-attachments/assets/e6ed3933-40c1-45ad-94bb-3b901ab32102)

# Overview
The files provided are a collection of code to help in getting a nixie clock working. This is mostly just a messy prototype so some of the code either does not fully function or is redundant. The main function which is to show time fully works as long as you have the following parts:
- Raspberry PICO - RP2040
- RTC module // The module I am using is the RTC DS1307 please find the appropriate drivers if you are using a different type
- 4x GC9A01 // Credit to the person that provided drivers for the displays below  

# Install
After uploading all the files into the PICO edit the code to support your RTC if it does not use the ds1307 module. 
Use the file labelled "refrshtest.py" to see if all the displays are appropriately connected. 
Set up the time via the file labelled "SetRTCtime.py."
Plug-in and play.

# Wiring
File: clock.py
- Full list of used GPIOs:
0, 1, 3, 4, 5, 6, 7, 8, 13, 14, 15, 17, 18, 19, 20, 21, 22, 25, 28, 29

Display Pins:
- TFT_SCK = 18 → SPI Clock
- TFT_MOSI = 19 → SPI MOSI

Display 1 (Hours Tens):
- TFT1_CS = 22
- TFT1_DC = 29
- TFT1_RES = 28

Display 2 (Hours Ones):
- TFT2_CS = 20
- TFT2_DC = 21
- TFT2_RES = 17

Display 3 (Minutes Tens):
- TFT3_CS = 5
- TFT3_DC = 4
- TFT3_RES = 3

Display 4 (Minutes Ones):
- TFT4_CS = 15
- TFT4_DC = 14
- TFT4_RES = 13

RTC Pins:
- I2C_SCL = 1
- I2C_SDA = 0

Buttons: // WARNING: these work but are essentially redundant because of the slow refresh rate on the screens, this makes changing the time via buttons very annoying. 
- set_time_button = 8
- increase_button = 6
- decrease_button = 7

Onboard LED:
- GPIO25 (internal LED pin)








# Drivers
https://github.com/russhughes/gc9a01_mpy
https://github.com/mcauser/micropython-tinyrtc-i2c/tree/master

GC9A01 Display driver in MicroPython based on devbis st7789py_mpy module from
https://github.com/devbis/st7789py_mpy modified to drive 240x240 pixel GC9A01
displays.
Documentation can be found at https://penfold.owt.com/gc9a01py/.
If you are looking for a faster driver with additional features, check out the
C version of the driver at https://github.com/russhughes/gc9a01_mpy
