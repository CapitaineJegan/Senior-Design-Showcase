import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 400, height = 400, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.grid()

def getCSV ():
    global df

    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv ('Oct 2019 raw schedule.csv')
    print(df)


browseButton_CSV = tk.Button(text="      Browse     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold')).grid(row=1,column=0)
searchbar = tk.Entry(root)
searchbar.grid(row=0, column=1)
tk.Label(root, text=" Search for File ", width=10).grid(row=0, column=0)

canvas1.create_window(200, 200, window=browseButton_CSV)

root.mainloop()
