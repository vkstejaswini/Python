import serial
ser = serial.Serial("COM3", 9600)   # open serial port that Arduino is using
print (ser)                         # print serial config
from tkinter import*
root=Tk()
def on() :
    print("on")
    print ("Sending serial data")
    ser.write(b"A")

def off():
    print("off")
    print ("Sending serial data")
    ser.write(b"B")

b=Button(root,text="on",bg="black",fg="red",command=on).pack()
b1=Button(root,text="off",bg="black",fg="red",command=off).pack()

mainloop()
