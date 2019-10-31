import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root= tk.Tk()
root.title('Upload Schedule')


inputvar = tk.StringVar(root)
def getCSV ():
    global full_df
    global xl

    import_file_path = filedialog.askopenfilename()
    full_df = pd.read_excel (import_file_path, usecols = 'A:F')
    #print(import_file_path)
    xl=pd.ExcelFile(import_file_path)

    inputvar.set(import_file_path)
    #print(full_df)
    #filePath.insert(0,inputvar)
    #print(inputvar)

filePath = tk.Entry(text = inputvar)
filePath.grid(row=0, column=0)

browseButton_CSV = tk.Button(text="      Browse     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold')).grid(row=0,column=1)
#searchbar = tk.Entry(root)
#searchbar.grid(row=0, column=1)
#tk.Label(root, text=" Upload Schedule").grid(row=0, column=0)
uploadButton = tk.Button(text = 'Upload')
uploadButton.grid(row=1, column=0, columnspan=2)
#canvas1.create_window(200, 200, window=browseButton_CSV)
tk.Label(root, text='Please specify sheetname').grid(row=3, column=0)
sheetname = tk.StringVar()
sheetbar = tk.Entry(root, textvariable=sheetname).grid(row=3, column=1)
def verifysheet():
    print(sheetname.get())
    print(xl.sheet_names)
    is_verified = False
    for i in xl.sheet_names:
        if i==sheetname.get():
            is_verified = True
    if is_verified == False:
        tk.messagebox.showerror('Error', 'Please enter a valid sheetname')
tk.Button(text = 'Verify', command=verifysheet).grid(row=4, column=0)

root.mainloop()
