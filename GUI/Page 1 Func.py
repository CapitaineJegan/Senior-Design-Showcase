import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ntpath
from tabulate import tabulate
from tkinter import *
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import numpy
import random

global df1 ###test variable for desk_filter function###
global p2aCategories # [Page2 LEFT] global list for desk entries 
global p2bCategories # [Page2 RIGHT] global list for desk entries

#global list values for the entries on Page 2
global deskList
global day1List
global origList
global destList
global day2List
global hourList

root= tk.Tk()   # [PAGE 1] The root window, Page 1
root.title('Upload Schedule')   # [PAGE 1] Title for Page 1

filePath = tk.StringVar()   # [Page 1] variable for file path

df= pd.read_csv('sep_2019 MELT.csv') #Test variable for fixing the dataframe file

##### [PAGE 1] Button message to check that the sheet name exists in the target file
def verifysheet():
    print(sheetname.get()) #gets and prints the sheet names
    print(xl.sheet_names)
    
    is_verified = False #by default, this is false until a valid sheet name is given
    
    for i in xl.sheet_names: #checks for validity of the entry for sheet name given in page 1
        if i==sheetname.get():
            is_verified = True
    
    if is_verified == False:
        tk.messagebox.showerror('Error', 'Please enter a valid sheetname')  #error message popup window if the given sheet name doesn't match the ones in the excel file
#####

#### [PAGE 1] Button for taking an excel file, melting, and showing the file path in the entry box
def getCSV():
    global melt #for storing the melted file as a variable to be used later
    global xl #file name; PLEASE USE ENTER x1 BEFORE USING VALIDATION!
    
    import_file_path = filedialog.askopenfilename()
#    df = pd.read_csv ('Oct 2019 raw schedule.csv')
    print(import_file_path)
#    df = pd.read_csv (import_file_path)

    '''
    Def:  unpivots the file on days as rows, removes international flights,
        removes rows without scheduled flights and removes unnecessary columns,
        datetime columns are added for departure, arrival, and release times,
        hour columns for each event are calculated from those columns,
        flight ID is added as a concatenation of Departure Datetime, Flight Number,
        Origin, and Destination
    Inputs:
        file: raw schedule Excel file
    Return: unpivoted dataframe with time formats and flight IDs
    '''
    #dataframe variables
    
    # create dataframes from Excel
    df = pd.read_excel(import_file_path) #CHANGE FILE AND SHEET NAMES
    
    # create airport list
    aiport_list = ['ABE', 'ABQ', 'AGS', 'ALB', 'ATL', 'ATW', 'AUS', 'AVL', 'AVP', 'BDL', 'BGR', 'BHM', 'BIL', 'BIS', 'BNA', 'BOI', 'BOS', 'BTR', 'BTV', 'BUF', 'BUR', 'BWI', 'BZN', 'CAE', 'CAK', 'CHA', 'CHO', 'CHS', 'CID', 'CLE', 'CLT', 'CMH', 'COS', 'CRW', 'CVG', 'DAB', 'DAL', 'DAY', 'DCA', 'DEN', 'DFW', 'DSM', 'DTW', 'ECP', 'EGE', 'ELP', 'EVV', 'EWR', 'EYW', 'FAR', 'FAY', 'FCA', 'FLL', 'FNT', 'FSD', 'GEG', 'GNV', 'GPT', 'GRB', 'GRR', 'GSO', 'GSP', 'GTF', 'HDN', 'HOU', 'HPN', 'HSV', 'IAD', 'IAH', 'ICT', 'ILM', 'IND', 'JAC', 'JAN', 'JAX', 'JFK', 'LAS', 'LAX', 'LEX', 'LFT', 'LGA', 'LGB', 'LIT', 'MCI', 'MCO', 'MDT', 'MDW', 'MEM', 'MHT', 'MIA', 'MKE', 'MLB', 'MOB', 'MSN', 'MSO', 'MSP', 'MSY', 'MTJ', 'MYR', 'OAK', 'OKC', 'OMA', 'ONT', 'ORD', 'ORF', 'PBI', 'PDX', 'PHF', 'PHL', 'PHX', 'PIT', 'PNS', 'PSC', 'PSP', 'PVD', 'PWM', 'RAP', 'RDU', 'RIC', 'RNO', 'ROA', 'ROC', 'RSW', 'SAN', 'SAT', 'SAV', 'SBN', 'SDF', 'SEA', 'SFO', 'SJC', 'SLC', 'SMF', 'SNA', 'SRQ', 'STL', 'SYR', 'TLH', 'TPA', 'TRI', 'TUL', 'TUS', 'TVC', 'TYS', 'VPS', 'XNA', 'YEG', 'YUL', 'YVR', 'YWG', 'YXE', 'YYC', 'YYZ']
    df = df[df['Org'].isin(aiport_list)]
    df = df[df['Dst'].isin(aiport_list)]

    # melts dataframe
    melt = pd.melt(df, id_vars=['Flt','Org','Dst','Eqt','Dptr','Arvl','BLK MINS','MILES','Desk']
        ,value_vars=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        ,var_name = 'Day'
        ,value_name = 'Schd')

    # drop not scheduled flights N/A
    melt = melt.dropna(subset=['Schd'])

    # set Year, Month and Date
    melt['Month'] =  10
    melt['Year'] =  2019
    melt['Date'] = pd.to_datetime(melt[['Year', 'Month', 'Day']])

    # make Departure, Arrival, and Release time columns
    melt['Dept_Time'] = pd.to_datetime(melt['Year'].astype(str) + '/' + melt['Month'].astype(str) + '/' + melt['Day'].astype(str) + ' ' +melt['Dptr'].astype(str),utc=True)
    melt['Arr_Time'] = pd.to_datetime(melt['Year'].astype(str) + '/' + melt['Month'].astype(str) + '/' + melt['Day'].astype(str) + ' ' +melt['Arvl'].astype(str),utc=True)
    melt['Rls_Time'] = melt['Dept_Time'] + pd.Timedelta(minutes=-90)

    melt = melt.drop(columns=['BLK MINS', 'Dptr','Arvl','Year', 'Month','Schd'])

    # make Hour Columns for each time
    melt['Rls_HR'] = melt['Rls_Time'].dt.hour
    melt['Dept_HR'] = melt['Dept_Time'].dt.hour
    melt['Arr_HR'] = melt['Arr_Time'].dt.hour
    
    melt['FltID'] = melt['Dept_Time'].astype(str) + melt['Flt'].astype(str) + melt['Org'].astype(str) + melt['Dst'].astype(str)
    
#    ntpath.basename(import_file_path)
    
    searchbar.delete(0, tk.END)
    searchbar.insert(0, import_file_path)
    
    filePath.set(import_file_path)
    
    xl=pd.ExcelFile(import_file_path)
    
#    print(df)
    print(melt)
    return melt


###Page 1 labels, boxes, and buttons###
tk.Label(root, text=" Search for File ",font=(12)).grid(row=0, column=0)

searchbar = tk.Entry(root, text=filePath.get(), width=50)
searchbar.grid(row=0, column=1)

browseButton_CSV = tk.Button(root, text="Browse", command=getCSV, bg='blue', fg='white', font=('helvetica', 12, 'bold')).grid(row=0,column=2, padx=5, sticky="W"+"E")

uploadButton = tk.Button(root, text="Load", bg='red', font=('helvetica', 12, 'bold'), command=makeP2)
uploadButton.grid(row=3, column=1, pady=10, sticky="W"+"E")

tk.Label(root, text='Please specify sheetname').grid(row=2, column=0)
sheetname = tk.StringVar()
sheetbar = tk.Entry(root, textvariable=sheetname, width=50).grid(row=2, column=1)

tk.Button(root, text = 'Verify', command=verifysheet, bg='blue', fg='white', font=('helvetica', 12, 'bold')).grid(row=2, column=2, padx=5, sticky="W"+"E")

root.geometry('%dx%d+%d+%d' % (550, 120, 500, 200))

root.mainloop()
###Page 1 Stuff END###