import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np

root= tk.Tk()
root.title('Upload Schedule')

#canvas1 = tk.Canvas(root, width = 400, height = 400, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.grid()
filePath = tk.Entry(root)
filePath.grid(row=0, column=0)
def getCSV ():
    global df

    import_file_path = filedialog.askopenfilename()
    df = pd.read_csv ('Oct 2019 raw schedule.csv')
    #print(df)
    filePath.insert(root, import_file_path)


browseButton_CSV = tk.Button(text="      Browse     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold')).grid(row=0,column=1)
#searchbar = tk.Entry(root)
#searchbar.grid(row=0, column=1)
#tk.Label(root, text=" Upload Schedule").grid(row=0, column=0)
uploadButton = tk.Button(text = 'Upload')
uploadButton.grid(row=1, column=0, columnspan=2)
#canvas1.create_window(200, 200, window=browseButton_CSV)

root.mainloop()
