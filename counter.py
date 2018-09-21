import tkinter as tk
global counter
counter=0
def update_func():
        global counter 
        counter = counter+1
        label.config(text=str(counter))
        label.after(1000, update_func)  # 1000ms

root = tk.Tk()
root.title("Counting Seconds")
label = tk.Label(root, fg="red")
label.pack()
start_counter(label)
button = tk.Button(root, text='Stop', width=30, command=root.destroy)
button.pack()
update_func()
root.mainloop()
