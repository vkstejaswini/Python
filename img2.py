from tkinter import *
import PIL.Image
import PIL.ImageTk

root = Tk()

im = PIL.Image.open("1.png")
photo = PIL.ImageTk.PhotoImage(im)

label = Label(root, image=photo)
label.image = photo  # keep a reference!
label.pack(side= LEFT)


im1 = PIL.Image.open("1.jpg")
photo1 = PIL.ImageTk.PhotoImage(im1)

label = Label(root, image=photo1)
label.image = photo1  # keep a reference!
label.pack( side=RIGHT)
mainloop()
