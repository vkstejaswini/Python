import serial
ser = serial.Serial("COM3", 9600)   # open serial port that Arduino is using
print (ser)
from tkinter import *
import PIL.Image
import PIL.ImageTk
class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

root = Tk()


def on() :
    
    print("on")
    print ("Sending serial data")
    ser.write(b"A")

def off():
    print("off")
    print ("Sending serial data")
    ser.write(b"B")
im = PIL.Image.open("1.png")
photo = PIL.ImageTk.PhotoImage(im)

#label = Label(root, image=photo)
#label.image = photo  # keep a reference!
#label.pack(side= LEFT)
#label.pack(command=on)


im1 = PIL.Image.open("1.jpg")
photo1 = PIL.ImageTk.PhotoImage(im1)

#label = Label(root, image=photo1)
#label.image = photo1  # keep a reference!
#label.pack(side=RIGHT)
#label.pack(command=off)
b=Button(root,image=photo,bg="black",fg="red", command=on).place(x=400,y=200)#.grid(row=0, column=0)
b1=Button(root,image=photo1,bg="black",fg="red",command=off).place(x=600,y=200)#.grid(row=50, column=30)
app=FullScreenApp(root)
root.mainloop()
