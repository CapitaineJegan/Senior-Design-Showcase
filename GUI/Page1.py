import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root= tk.Tk()
root.title('Upload Schedule')


inputvar = tk.StringVar(root)
def getCSV ():
    global full_df

    import_file_path = filedialog.askopenfilename()
    full_df = pd.read_excel (import_file_path, usecols = 'A:F')
    #print(import_file_path)

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

root.mainloop()
