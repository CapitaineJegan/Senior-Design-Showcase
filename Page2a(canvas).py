import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root=tk.Tk()
root.title('Desks')
canvas1 = tk.Canvas(root, width = 800, height = 400)
canvas1.pack()
entry_day = tk.Entry(root)
canvas1.create_window(200,140, window = entry_day)
#tk.Label(root, text = 'Desks', width = 10)#.grid(row=0, column=0)
#tk.Label(root, text = 'Day:', width = 10)#.grid(row=1, column=0)
def getDay():
    day = entry_day.get()
    try:
        int(day)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer')
    if int(day)<=0 or int(day)>31:
        tk.messagebox.showerror('Error', 'Please enter a valid number')
button1 = tk.Button(text='Next', command = getDay)
canvas1.create_window(200,200, window = button1)
label_day = tk.Label(root, text = 'day')
canvas1.create_window(120,140, window = label_day)
label_desks = tk.Label(root, text = 'Desks')
canvas1.create_window(200, 70, window = label_desks)
root.mainloop()
