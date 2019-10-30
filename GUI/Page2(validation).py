import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root=tk.Tk()
root.title('Desks')
#entry_day = tk.Entry(root)
#entry_day.grid(row =1, column =1)
tk.Label(root, text = 'Desks').grid(row=0, column=0, columnspan = 2, sticky=tk.W+tk.E)
tk.Label(root, text = 'Day').grid(row=1, column=0)
def getDay():
    day = entry_day.get()
    try:
        int(day)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer')
    if int(day)<=0 or int(day)>31:
        tk.messagebox.showerror('Error', 'Please enter a valid number')
def only_numbers(char):
    return char.isdigit()

validation = root.register(only_numbers)
entry = tk.Entry(root, validate="key", validatecommand=(validation, '%S'),font=("Helvetica", 16), bg = 'black',fg = 'light green').grid(row =1, column =1)
button1 = tk.Button(text='Next').grid(row = 2, column =0, columnspan =2)
root.mainloop()
