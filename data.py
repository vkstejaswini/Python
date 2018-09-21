import serial
import sys
import time
import tkinter as tk
root = tk.Tk()
path="interior.jpg"
background_image=tk.PhotoImage(path)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
ser = serial.Serial('com3', 9600, timeout=1)
def start_counter(label,label2,label3):
    def update_func():
        global reading
        reading =ser.readline().decode('utf-8')[:-2]
        reading=str(reading)
        print(reading)
        arr=reading.split(',')
        label.config(text=str(arr[0]))
        label2.config(text=str(arr[1]))
        label3.config(text=str(arr[2]))
        label.after(1000, update_func)  # 1000ms
        time.sleep(1)
    update_func()

root.title("Room Monitoring System")
temp=tk.Label(root,text="ROOM MONITORING SYSTEM",font=100, fg="blue").place(x=500,y=150)
temp=tk.Label(root,text="TEMPERATURE",font=40, fg="blue").place(x=100,y=300)
temp=tk.Label(root,text="HUMIDITY", font=40,fg="blue").place(x=500,y=300)
temp=tk.Label(root,text="GAS / SMOKE",font=0 ,fg="blue").place(x=900,y=300)
label = tk.Label(root, font=20,fg="red")
label.place(x=100,y=400)
label2 = tk.Label(root,font=20 ,fg="green")
label2.place(x=500,y=400)
label3 = tk.Label(root,font=20 ,fg="grey")
label3.place(x=900,y=400)
start_counter(label,label2,label3)
button = tk.Button(root, text='Stop', width=30, command=root.destroy)
button.place(x=600,y=600)
root.mainloop()



        
    
    
  
   
   










