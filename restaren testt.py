from tkinter import *
global count
def main():
    i=0
    j=0
    b[i][j] = Button(font=('Verdana', 40), width=10,bg='red',text='veg', command=lambda r=i, c=j: callback(r,c))
    b[i][j].grid(row=i, column=j)
    i=0
    j=1
    b[i][j] = Button(font=('Verdana', 40), width=10,bg='green', text='non veg',command=lambda r=i, c=j: callback(r,c))
    b[i][j].grid(row=i, column=j)
    i=0
    j=2
    b[i][j] = Button(font=('Verdana', 40), width=10,bg='orange', text='cool drinks',command=lambda r=i, c=j: callback(r,c))
    b[i][j].grid(row=i, column=j)
    i=1
    j=0
    b[i][j] = Button(font=('Verdana', 40), width=10,bg='yellow', text='ice creams',command=lambda r=i, c=j: callback(r,c))
    b[i][j].grid(row=i, column=j)
    i=1
    j=1
    b[i][j] = Button(font=('Verdana', 40), width=10,bg='brown', text='salads',command=lambda r=i, c=j: callback(r,c))
    b[i][j].grid(row=i, column=j)
def callback(r,c):
    print (str(r)+':'+str(c))
    if r==0 and c==0:
        item=[['special menu','Breakfast','lunch'],
              ['soups','staturs','main-course'],
              ['dinner','Back','snacks']
              ]
        for i in range(3):
            for j in range(3):
                b[i][j] = Button(font=('Verdana', 40), width=10,bg='green',text=item[i][j] ,command=lambda r=i, c=j: callback(r,c))
                b[i][j].grid(row=i, column=j)
                
    if r==2 and c==1: 
                        main()
b = [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]
     ]
root=Tk()
main()
root.mainloop()
