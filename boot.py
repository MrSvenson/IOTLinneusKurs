import pycom
from network import Bluetooth
from machine import UART
import machine
import os

uart = UART(0, baudrate=115200)
os.dupterm(uart)

# Disable bluetooth to save power
bluetooth = Bluetooth()
bluetooth.deinit()

machine.main('main.py')

