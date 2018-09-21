from Tkinter import *
import PIL.Image
import PIL.ImageTk

root = Toplevel()

im = PIL.Image.open("1.png")
photo = PIL.ImageTk.PhotoImage(im)

label = Label(root, image=photo)
label.image = photo  # keep a reference!
label.pack()

root.mainloop()
