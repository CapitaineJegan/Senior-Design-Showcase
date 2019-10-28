import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import ntpath #for taking file name only - still working on that.
#
#window = tk.Tk()
#window.title('Upload Schedule')
#window.mainloop()

root= tk.Tk()
root.title('Upload Schedule')

filePath = tk.StringVar()
global df
global p2Categories

def getCSV():#for taking the csv files in the first page button
    import_file_path = filedialog.askopenfilename()
#    df = pd.read_csv ('Oct 2019 raw schedule.csv')
    print(import_file_path)
    df = pd.read_excel (import_file_path, usecols='A:F')

#    ntpath.basename(import_file_path)

    searchbar.delete(0, tk.END)
    searchbar.insert(0, import_file_path)

    filePath.set(import_file_path)

    print(df)

def savep2Info(p1,p2,p3,p4,a1,a2,a3,a4):
    p2Categories = []
    p2Categories.append(p1)
    p2Categories.append(p2)
    p2Categories.append(p3)
    p2Categories.append(p4)
    print(p2Categories)
    if len(p1) != 3 or p1.isalpha() == False:
        tk.messagebox.showerror('Error', 'Please enter string with 3 letters for origin station')
    if len(p2) != 3 or p2.isalpha() == False:
        tk.messagebox.showerror('Error', 'Please enter string with 3 letters for destination station')
    try:
        int(p3)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer for day of the month')
    if int(p3)<=0 or int(p3)>31:
        tk.messagebox.showerror('Error', 'Please enter a valid number for day of the month')
    try:
        int(p4)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer for hour')
    if int(p4)<0 or int(p4)>23:
        tk.messagebox.showerror('Error', 'Please enter a valid number for hour')

def makeP2():
    ###Page 2a and 2b code###
    page2b=tk.Toplevel()
    page2b.title("Desks & Flights")

    #variables for the entries in 2b, basically what you'd type in to search.
    p2orig = tk.StringVar(page2b)
    p2dest = tk.StringVar(page2b)
    p2day2 = tk.StringVar(page2b)
    p2hour = tk.StringVar(page2b)

    #stores a value for if the All boxes are ticked. 1 is True, 0 is False.
    origAll = tk.IntVar()
    destAll = tk.IntVar()
    day2All = tk.IntVar()
    hourAll = tk.IntVar()

    ###Page 2a code###
#    canvas1 = tk.Canvas(page2b, width = 400, height = 400)
#    canvas1.pack()
#    entry1 = tk.Entry(page2b)
#    entry1.grid(row=1, column=1)
#    tk.Label(page2b, text="Desks", width = 10).grid(row=0, column=0, columnspan=2)
#    tk.Label(page2b, text="Day:", width = 10).grid(row=1, column=0)
    entry_day = tk.Entry(page2b)
    entry_day.grid(row =1, column =1)
    tk.Label(page2b, text = 'Desks').grid(row=0, column=0, columnspan = 2, sticky=tk.W+tk.E)
    tk.Label(page2b, text = 'Day').grid(row=1, column=0, sticky="W")
    ###Page 2a code end###

    #canvas1 = tk.Canvas(root, width=800,height=400).grid()
    #Flights label, pair on the right side of Desks with column span of 3 instead of 2
    #to accommodate the "All" checkboxes
    tk.Label(page2b, text="Flights").grid(row=0, column=2, columnspan=3, sticky="W"+"E")

    #Origin
    tk.Label(page2b, text="Origin").grid(row=1, column=2, sticky="W")
    entryOrig = tk.Entry(page2b, textvariable = p2orig)
    entryOrig.grid(row=1, column=3)
    #listbox = tk.OptionMenu(root, orig, 1)
    #listbox.grid(row=1, column=3)
    cOrig = tk.Checkbutton(page2b, text="All", variable=origAll)
    cOrig.grid(row=1, column=4)

    #Destination
    tk.Label(page2b, text="Destination").grid(row=2, column=2, sticky="W")
    entryDest = tk.Entry(page2b, textvariable = p2dest)
    entryDest.grid(row=2, column=3)
    #listbox = tk.OptionMenu(root, dest,2,3)
    #listbox.grid(row=2, column=3)
    cDest = tk.Checkbutton(page2b, text="All", variable=destAll)
    cDest.grid(row=2, column=4)

    #Day
    tk.Label(page2b, text="Day").grid(row=3, column=2, sticky="W")
    entryDay2 = tk.Entry(page2b, textvariable = p2day2)
    entryDay2.grid(row=3, column=3)
    #listbox = tk.OptionMenu(root, day2,2,3)
    #listbox.grid(row=3, column=3)
    cDay = tk.Checkbutton(page2b, text="All", variable=day2All)
    cDay.grid(row=3, column=4)

    #Hour
    tk.Label(page2b, text="Hour").grid(row=4, column=2, sticky="W")
    entryHour = tk.Entry(page2b, textvariable = p2hour)
    entryHour.grid(row=4, column=3)
    #listbox = tk.OptionMenu(root, hour,2,3)
    #listbox.grid(row=4, column=3)
    cHour = tk.Checkbutton(page2b, text="All", variable=hourAll)
    cHour.grid(row=4, column=4)

    tk.Button(page2b, text="Back", command=lambda: page2b.destroy()).grid(row=5, column=0, sticky="W"+"E") #Back button

    p2Next = tk.Button(page2b, text="Next", command=lambda: savep2Info(p2orig.get(),p2dest.get(),p2day2.get(),p2hour.get(),origAll.get(),destAll.get(),day2All.get(),hourAll.get()))
    p2Next.grid(row=5, column=3, columnspan=2, sticky="W"+"E") #Next button
    ###Page 2b code end###


#will incorporate these two checks for accuracy of entries later this week
def checkday(day):
    try:
        int(day)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer for day of the month')
    if int(day)<=0 or int(day)>31:
        tk.messagebox.showerror('Error', 'Please enter a valid number for day of the month')

def checkhour(hour):
    try:
        int(hour)
    except:
        tk.messagebox.showerror('Error', 'Please enter an integer for hour')
    if int(hour)<0 or int(hour)>23:
        tk.messagebox.showerror('Error', 'Please enter a valid number for hour')

canvas1 = tk.Canvas(root, width = 400, height = 400, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.grid()

tk.Label(root, text=" Search for File ", width=10).grid(row=0, column=0)

searchbar = tk.Entry(root, text=filePath.get())
searchbar.grid(row=0, column=1)

browseButton_CSV = tk.Button(text="      Browse     ", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold')).grid(row=1,column=0)
canvas1.create_window(200, 200, window=browseButton_CSV)

uploadButton = tk.Button(text="Upload", command=makeP2)
uploadButton.grid(row=1, column=1, sticky="W"+"E"+"N"+"S")

root.mainloop()
