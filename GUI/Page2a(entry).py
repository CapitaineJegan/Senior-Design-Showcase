import tkinter as tk
#from tkinter import fieldialog
#import pandas as pd
#import numpy as np

root=tk.Tk()
root.title("Flights")

listOrig = [1,2,3,4,5,6] #still working on this part; should take in the list
#of origins and show them in the Origin drop down - Leon

orig = tk.StringVar(root)
dest = tk.StringVar(root)
day = tk.StringVar(root)
hour = tk.StringVar(root)

origAll = tk.IntVar()
destAll = tk.IntVar()
dayAll = tk.IntVar()
hourAll = tk.IntVar()

#canvas1 = tk.Canvas(root, width=800,height=400).grid()
#Flights label, pair on the right side of Desks with column span of 3 instead of 2
#to accommodate the "All" checkboxes
tk.Label(root, text="Flights").grid(row=0, column=2, columnspan=3, sticky="W"+"E")

#Origin
tk.Label(root, text="Origin").grid(row=1, column=2, sticky="W")
tk.Entry(root).grid(row=1, column=3)
#listbox = tk.OptionMenu(root, orig, listOrig)
#listbox.grid(row=1, column=3)
cOrig = tk.Checkbutton(root, text="All", variable=origAll)
cOrig.grid(row=1, column=4)

#Destination
tk.Label(root, text="Destination").grid(row=2, column=2, sticky="W")
tk.Entry(root).grid(row=2, column=3)
#listbox = tk.OptionMenu(root, dest,2,3)
#listbox.grid(row=2, column=3)
cDest = tk.Checkbutton(root, text="All", variable=destAll)
cDest.grid(row=2, column=4)

#Day
tk.Label(root, text="Day").grid(row=3, column=2, sticky="W")
tk.Entry(root).grid(row=3, column=3)
#listbox = tk.OptionMenu(root, day,2,3)
#listbox.grid(row=3, column=3)
cDay = tk.Checkbutton(root, text="All", variable=dayAll)
cDay.grid(row=3, column=4)

#Hour
tk.Label(root, text="Hour").grid(row=4, column=2, sticky="W")
tk.Entry(root).grid(row=4, column=3)
#listbox = tk.OptionMenu(root, hour,2,3)
#listbox.grid(row=4, column=3)
cHour = tk.Checkbutton(root, text="All", variable=hourAll)
cHour.grid(row=4, column=4)

def checkday():
    try:
        int(day)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer for day of the month')
    if int(day)<=0 or int(day)>31:
        tk.messagebox.showerror('Error', 'Please enter a valid number for day of the month')
def checkhour():
    try:
        int(hour)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer for hour')
    if int(day)<0 or int(day)>23:
        tk.messagebox.showerror('Error', 'Please enter a valid number for hour')

tk.Button(root, text="Next").grid(row=5, column=2, columnspan=3, sticky="W"+"E")

root.mainloop()
