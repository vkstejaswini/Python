import serial
ser = serial.Serial("COM3", 9600)   # open serial port that Arduino is using
print (ser)                         # print serial config
from tkinter import*
root=Tk()
frame = Frame(root, width=500, height=500)
frame.pack()
def on() :
    print("on")
    print ("Sending serial data")
    ser.write(b"A")

def off():
    print("off")
    print ("Sending serial data")
    ser.write(b"B")
tmp1 = PhotoImage(file='bulbon.png')
buttonStart1 = Button(frameWb,image=tmp1,command=on).pack()
tmp2 = PhotoImage(file='bulboff.png')
buttonStart2 = Button(frameWb,image=tmp2,command=off).pack()


mainloop()
