from tkinter import *
 
master = Tk()
master.minsize(300,100)
master.geometry("320x100")
 
def callback():
    print("click!")
 
 
photo=PhotoImage(file="bulboff.jpg")
b = Button(master,image=photo, command=callback, height=50, width=150)
b.pack()
 
mainloop()
