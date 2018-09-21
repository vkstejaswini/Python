import serial
import sys
import time
import tkinter as tk

ser = serial.Serial('com3', 9600, timeout=1)


while True:
        global reading
        reading =ser.readline().decode('utf-8')[:-2]
        reading=str(reading)
        print(reading)
        a=reading.split(',')
        print(a)
        print(a[0])
        print(a[1])
        print(a[2])
        time.sleep(1)




        
    
    
  
   
   










