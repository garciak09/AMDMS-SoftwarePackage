#!/usr/bin/env python3
"""Control an Arduino over the USB port."""

# Referenced Website : https://www.woolseyworkshop.com/2020/02/05/controlling-an-arduino-from-a-raspberry-pi/

# usb.py
# Created by John Woolsey on 12/17/2019.
# Copyright (c) 2019 Woolsey Workshop.  All rights reserved.


# USB_PORT = "/dev/tty.usbmodem12101"  # On MAC
USB_PORT = "/dev/ttyACM0"  # On RPi

## Run this file with ./usb.py
## From there you can enter commands to receive input from the arduino

# Imports
import serial
import PySimpleGUI as sg


# Main
def runArduinoScript(window, onlyCentering=False):
    if onlyCentering:
        string = '-CENTERING-THREAD-'
    else:
        string = '-THREAD-'
    # Connect to USB serial port at 9600 baud
    try: 
        window.write_event_value((string, 'Alignment in Progress'), 'Alignment in Progress')
        usb = serial.Serial(USB_PORT, 9600, timeout=2)


        # Send commands to Arduino
        # print("Enter a command from the keyboard to send to the Arduino.")
        # print_commands()

        file = open("arduinoOutput.txt", "w")
        usb.write(b'go\n')
        while True:
            # command = input("Enter command: ")
            line = usb.readline()  # read input from Arduino
            line = line.decode()  # convert type from bytes to string
            line = line.strip()  # strip extra whitespace characters
            if len(line) == 0:
                continue
            print(line)
            if line == "DONE" or line == "5":
                window.write_event_value((string, 'Mirror Aligned'), 'Mirror Aligned')
                break
            file.write(line + "\n")
    except:
        print("failed")
        window.write_event_value((string, 'Alignment Failed'), 'Alignment Failed')