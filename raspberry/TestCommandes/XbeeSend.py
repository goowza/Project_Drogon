#!/usr/bin/env python
import time
import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1             
 )
counter=0       
      
while 1:
    steer_command = input("Send command (0 = left | 1 = right)")
    ser.write(str.encode(steer_command))
    time.sleep(1)
    counter += 1
