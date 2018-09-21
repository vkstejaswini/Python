import serial
import sys
import time
import tkinter as tk

ser = serial.Serial('com3', 9600, timeout=1)
def start_counter(label):
    def update_func():
        global reading
        reading =ser.readline().decode('utf-8')[:-2]
        reading=str(reading)
        print(reading)
        arr=reading.split(',')
        label.config(text=str(arr[0]))
        #l2.config(text=arr[1])
        #l3.config(text=arr[2])
        l1.after(1000, update_func)  # 1000ms
    update_func()

'''while True:
        global reading
        reading =ser.readline().decode('utf-8')[:-2]
        reading=str(reading)
        print(reading)
        a=reading.split(',')
        print(a)
        print(a[0])
        print(a[1])
        print(a[2])'''
root = tk.Tk()
root.title("Counting Seconds")
label = tk.Label(root, fg="red").pack()#side=LEFT)
#l2 = tk.Label(root, fg="red").pack()#side=CENTER)
#l3 = tk.Label(root, fg="red").pack()#side=RIGHT)
start_counter(label)#,l2,l3)
button = tk.Button(root, text='Stop', width=30, command=root.destroy)
button.pack()
root.mainloop()



        
    
    
  
   
   










