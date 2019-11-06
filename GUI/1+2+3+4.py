import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import ntpath #for taking file name only - still working on that.
from tabulate import tabulate
from tkinter import *
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#importing filters
import csv
import numpy
import random
import numpy as np

#window = tk.Tk()
#window.title('Upload Schedule')
#window.mainloop()

root= tk.Tk()
root.title('Upload Schedule')

filePath = tk.StringVar()
inputvar = tk.StringVar(root)
global df###test variable for dataframe!###
global p2Categories
global melt
global file
global desk
#global list values for the entries on Page 2
global deskList
global day1List
global origList
global destList
global day2List
global hourList
#deskList = []
#day1List = []
#origList = []
#destList = []
#day2List = []
#hourList = []

#####Button message to check that the sheet name exists in the target file
def verifysheet():
    print(sheetname.get())
    print(xl.sheet_names)
    is_verified = False
    for i in xl.sheet_names:
        if i==sheetname.get():
            is_verified = True
    if is_verified == False:
        tk.messagebox.showerror('Error', 'Please enter a valid sheetname')
#####

def getCSV():#for taking the csv files in the first page button
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
    global melt
    global xl


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
    #print(melt)
    return melt

#Page 2 Next button functions. Order is desk, day1 info is p1, p2, and origin, destination, day2, and hour are p3, p4, p5,and p6
def savep2dskInfo(page, p1, p2):
    p2Categories = []
    p2Categories.append(p1)
    p2Categories.append(p2)
    print(p2Categories)

    deskList = []
    day1List = []

    deskList = list(p1.split(","))
    day1List = list(p2.split(","))

    try:
        day1List = list(map(int, day1List))

    except:
        print()

    print(deskList, day1List)
    page.destroy()
    makeP3a()

#saves the information on page 2 for Flight side, then closes the window and moves onto page 3b, similar to above function for Desk and page 3a
def savep2fltInfo(page, p3, p4, p5, p6):
    p2Categories = []
    p2Categories.append(p3)
    p2Categories.append(p4)
    p2Categories.append(p5)
    p2Categories.append(p6)
    #print(p5)

    print(p2Categories)


    origList = []
    destList = []
    day2List = []
    hourList = []

    origList = list(p3.split(","))
    destList = list(p4.split(","))
    day2List = list(p5.split(","))
    hourList = list(p6.split(","))

#    for orig in origList:
 #       if len(orig) != 3:
  #          tk.messagebox.showerror('Error', 'Please enter a valid origin')
    if origList == ['']:
         origList = []
#    for dest in destList:
#        if len(dest) != 3:
#            tk.messagebox.showerror('Error', 'Please enter a valid destination')'''
    if destList == ['']:
        destList = []
    for day in day2List:
        try:
            int(day)
        except:
            tk.messagebox.showerror('Error', 'Please enter an integer for day of the month')
        if int(day)<=0 or int(day)>31:
            tk.messagebox.showerror('Error', 'Please enter a valid number for day of the month')
    for hour in hourList:
        try:
            int(hour)
        except:
            tk.messagebox.showerror('Error', 'Please enter an integer for hour')
        if int(hour)<0 or int(hour)>23:
            tk.messagebox.showerror('Error', 'Please enter a valid number for hour')
    try:
        day2List = list(map(int, day2List))

    except:
        print()

    print(origList, destList, day2List, hourList)
    page.destroy()
    makeP3b(origList, destList, day2List, hourList)

#Page 2 functions
def makeP2():
    ###Page 2a and 2b code###
    page2b=tk.Toplevel()
    page2b.title("Desks & Flights")

    page2b.geometry('%dx%d+%d+%d' % (780, 200, 500, 200))

    #variables for the entries in 2b, basically what you'd type in to search.
    p2desk = tk.StringVar(page2b)
    p2day1 = tk.StringVar(page2b)
    p2orig = tk.StringVar(page2b)
    p2dest = tk.StringVar(page2b)
    p2day2 = tk.StringVar(page2b)
    p2hour = tk.StringVar(page2b)

    #stores a value for if the All boxes are ticked. 1 is True, 0 is False. *Might not need*
#    origAll = tk.IntVar()
#    destAll = tk.IntVar()
#    day2All = tk.IntVar()
#    hourAll = tk.IntVar()

    ###Page 2a code###
    tk.Label(page2b, text = 'Desks',font=('helvetica', 16)).grid(row=0, column=0, columnspan = 3, sticky="W"+"E") #Header for Desks

    tk.Label(page2b, text = 'Desk',font=('helvetica', 14)).grid(row=1, column=0, sticky="W")
    entryDesk = tk.Entry(page2b, textvariable = p2desk, width=50)
    entryDesk.grid(row=1, column=1, columnspan=2)

    tk.Label(page2b, text = 'Day',font=('helvetica', 14)).grid(row=2, column=0, sticky="W")
    entry_day = tk.Entry(page2b, textvariable = p2day1, width=50)
    entry_day.grid(row=2, column=1, columnspan=2)


    p2Nextdsk = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2dskInfo(page2b, p2desk.get(), p2day1.get()))
    p2Nextdsk.grid(row=3, column=1, sticky="W"+"E") #Next button for desks (left side)

    ###Page 2a code end###

    #canvas1 = tk.Canvas(root, width=800,height=400).grid()
    #Flights label, pair on the right side of Desks with column span of 3 instead of 2
    #to accommodate the "All" checkboxes
    tk.Label(page2b, text="Flights",font=('helvetica', 16)).grid(row=0, column=3, columnspan=4, sticky="W"+"E") #Header for Flights

    #Origin
    tk.Label(page2b, text="Origin",font=('helvetica', 14)).grid(row=1, column=3, sticky="W")
    entryOrig = tk.Entry(page2b, textvariable = p2orig, width=50)
    entryOrig.grid(row=1, column=4, columnspan=2)

    #Destination
    tk.Label(page2b, text="Destination",font=('helvetica', 14)).grid(row=2, column=3, sticky="W")
    entryDest = tk.Entry(page2b, textvariable = p2dest, width=50)
    entryDest.grid(row=2, column=4, columnspan=2)

    #Day, int
    tk.Label(page2b, text="Day",font=('helvetica', 14)).grid(row=3, column=3, sticky="W")
    entryDay2 = tk.Entry(page2b, textvariable = p2day2, width=50)
    entryDay2.grid(row=3, column=4, columnspan=2)

    #Hour, string
    tk.Label(page2b, text="Hour",font=('helvetica', 14)).grid(row=4, column=3, sticky="W")
    entryHour = tk.Entry(page2b, textvariable = p2hour, width=50)
    entryHour.grid(row=4, column=4, columnspan=2)

    tk.Button(page2b, text="Back",font=('helvetica', 12), command=lambda: page2b.destroy()).grid(row=5, column=0, sticky="W"+"E") #Back button

    p2Nextflt = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2fltInfo(page2b, p2orig.get(), p2dest.get(), p2day2.get(), p2hour.get()))
    p2Nextflt.grid(row=5, column=4, sticky="W"+"E") #Next button for flights (right side)
    ###Page 2b code end###

def p3aclose(p3):
    p3.destroy()
    makeP2()

def p3bclose(p3):
    p3.destroy()
    makeP2()

def p3arefresh(p3):
    p3.destroy()
    makeP3a()

def p3brefresh(p3):
    p3.destroy()
    makeP3b(origList, destList, day2List, hourList)

#Page 3 functions
###TK for Page 3 scrollbar class###
df= pd.read_csv('sep_2019 MELT.csv')


#desk filter
def desk_filter(day,desk):
    global df2
    desk_new=[]
    for i in desk:
        desk_new.append(str(i))
    df1= df[df.Day.isin(day)]
    df2=df1[df1.Desk.isin(desk_new)]  #needs to be a string
    return (df2)

desk_filter([1],[3])
#print(df2)


#flight filter
def flight_filter(df, org,dest,day_,hour_):
    day=[]
    hour=[]
    for d in day_:
        day.append(np.int64(d))
    for h in hour_:
        hour.append(np.int64(h))


#     return(len(org),len(dest),len(day),len(hour))
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)>0:  #no org

        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
#         return(type(df['Org'][0]),type(df['Dst'][0]),type(df['Day'][1])==numpy.int64,type(df['RlsHR'][1])==numpy.int64)
        return fl3


    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no dest
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3

    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        return fl3

    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no org,dest
        fl1=df[df.Day.isin(day)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no org,day
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no org,hour
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #no dest,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2
    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #no dest,day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #no day,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #only org
        fl1=df[df.Org.isin(org)]
        return fl1
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #only dest
        fl1=df[df.Dst.isin(dest)]
        return fl1
    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #only day
        fl1=df[df.Day.isin(day)]
        return fl1
    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #only hour
        fl1=df[df.Rls_HR.isin(hour)]
        return fl1

    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #none entered
        return df
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)>0:
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        fl4=fl3[fl3.Rls_HR.isin(hour)]
        return fl4

#Other data functions
def melt_file(file):

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

    # create dataframes from Excel
    df = pd.read_excel(file, sheet_name='DOM') #CHANGE FILE AND SHEET NAMES

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

    return melt


def graphdesk(desk):
    #placeholder dataframes
    #global desk
    newWindow = tk.Toplevel()
    newWindow.title("Visualizer")

    newWindow.geometry('%dx%d+%d+%d' % (1800, 800, 100, 100))

    ###Jake's 'Graph from Data' code###
    file = 'sep_2019.xlsx'

    global melt
    melt = melt_file(file)
    global date
    date = '10-01-2019'
    global desks
    desks = ['M87', 1]
    global desk_filter_data
    desk_filter_data = desk_filter(melt, date, desks)
    global desk_display_df
    desk_display_df = desk_display(melt, date, desks)
    desk = 'M87'
    workload_dist(desk, newWindow)
    releases_dist(desk, newWindow)
    cities_dist(desk_filter_data, newWindow)


class VerticalScrolledFrame(Frame):
        """A pure Tkinter scrollable frame that actually works!
        * Use the 'interior' attribute to place widgets inside the scrollable frame
        * Construct and pack/place/grid normally
        * This frame only allows vertical scrolling"""
        def __init__(self, parent, *args, **kw):
            Frame.__init__(self, parent, *args, **kw)

            # create a vertical scrollbar for scrolling it
            vscrollbar = Scrollbar(self, orient=VERTICAL)
            vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

            # create a horizontal scrollbar and the canvas
#            hscrollbar = Scrollbar(self, orient=HORIZONTAL)
#            hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
            canvas = Canvas(self, bd=0, highlightthickness=0, width=2500, height=800, yscrollcommand=vscrollbar.set)#, xscrollcommand=hscrollbar.set)
            canvas.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=W)
            vscrollbar.config(command=canvas.yview)
#            hscrollbar.config(command=canvas.xview)

            # reset the view
#            canvas.xview_moveto(0)
            canvas.yview_moveto(0)

            # create a frame inside the canvas which will be scrolled with it
            self.interior = interior = Frame(canvas)
            interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

            # track changes to the canvas and frame width and sync them,
            # also updating the scrollbar
            def _configure_interior(event):
                # update the scrollbars to match the size of the inner frame
                size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
                canvas.config(scrollregion="0 0 %s %s" % size)
                if interior.winfo_reqwidth() != canvas.winfo_width():
                    # update the canvas's width to fit the inner frame
                    canvas.config(width=interior.winfo_reqwidth())
            interior.bind('<Configure>', _configure_interior)

            def _configure_canvas(event):
                if interior.winfo_reqwidth() != canvas.winfo_width():
                    # update the inner frame's width to fill the canvas
                    canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            canvas.bind('<Configure>', _configure_canvas)


###//Page 3 scrollbar class###

def makeP3a():
    page3a = tk.Toplevel()
    page3a.geometry('%dx%d+%d+%d' % (500, 880, 400, 80))

    p3frame = VerticalScrolledFrame(page3a)
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)

    deskNum=tk.StringVar()

    #visualization for graphs
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0, sticky='e')
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w')
    headers = []

    #Hardcoding random variables; will replace with max_XXX functions in next version
    for x in range(100):

        a=random.randint(1,20)
        b=random.randint(1,20)
        c=random.randint(1,20)

        if a > 10 or b > 10 or c > 5:
            tk.Label(p3frame.interior, text=random.randint(1,100), font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=0, sticky='w'+'e')
            tk.Label(p3frame.interior, text=a, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=1, sticky='w'+'e')
            tk.Label(p3frame.interior, text=b, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=2, sticky='w'+'e')
            tk.Label(p3frame.interior, text=c, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=3, sticky='w'+'e')
        else:
            tk.Label(p3frame.interior, text=random.randint(1,100), font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=0, sticky='w'+'e')
            tk.Label(p3frame.interior, text=a, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=1, sticky='w'+'e')
            tk.Label(p3frame.interior, text=b, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=2, sticky='w'+'e')
            tk.Label(p3frame.interior, text=c, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=3, sticky='w'+'e')


    ##########

#    df2.to_csv('headless.csv', header=False, index=False)
#
#    file = 'sep_2019.xlsx'
#
#    melt = melt_file(file)
#    date = '10-01-2019'
#    desks = ['M87', 1]
#    desk_filter_data = desk_filter(melt, date, desks)
#
#    p3aRls = max_rls(event_hours(desk_filter_data))
#    p3aFlt = max_flights(event_hours(desk_filter_data))
#    p3aCit = max_cities(event_hours(desk_filter_data))
#
#    print(p3aRls)
#    print(p3aFlt)
#    print(p3aCit)

#    tk.Label(page3, text="Desk #").grid(row=1, column=1, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Releases/hr").grid(row=1, column=2, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Flights/hr").grid(row=1, column=3, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Stations/hr").grid(row=1, column=4, sticky="W"+"E")
    headers = ['Desk#', 'Max. # of Releases/hr', 'Max # of Flights/hr', 'Max # of Stations/hr']
    headerindex = 0

    for i in headers:
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 12), bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1

#    listedDF = df2.values.tolist()
#    i_index = 2
#    j_index = 0
#
#    for i in listedDF:
#        for j in i:
#            if i[0] < 101:
#                tk.Label(p3frame.interior, text=j,font=("Helvetica", 8),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
#            else:
#                tk.Label(p3frame.interior,text=j,font=("Helvetica", 8),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
#            j_index +=1
#        i_index +=1
#        j_index = 0

    tk.Button(page3a,text="Refresh", font=('helvetica', 12), command=lambda: p3arefresh(page3a)).grid(row=0,column=1, sticky="E")
    tk.Button(page3a, text="Back", font=('helvetica', 12), command=lambda: p3aclose(page3a)).grid(row=3, column=0, sticky="W")

def makeP3b(origList,destList,day2List,hourList):
    page3b = tk.Toplevel()
    page3b.geometry('%dx%d+%d+%d' % (1380, 890, 400, 80))

    p3frame = VerticalScrolledFrame(page3b)
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)
    #self.label = Label(text="Shrink the window to activate the scrollbar.")
    #self.label.grid(row=1, column=0)

    deskNum=tk.StringVar()

    #visualization for graphs
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0)
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w'+'e')
    headers = []

    #variables for testing
    org=['ATL']
    dest=['MEM']
    day_=[2,3]
    hour_=[2]
    ###
    for day in day2List:
        day = int(day)
    for hour in hourList:
        hour = int(hour)
    ###printing
    print(origList)
    print (destList)
    print(day2List)
    print(hourList)
    #actualy entries
    org = origList
    dest= destList
    day_ = day2List
    hour_ = hourList

    filtered_flights = flight_filter(df, org,dest,day_,hour_)
    print('flight filter entries',org,dest,day_,hour_)
    print(filtered_flights)
    ###

    for col in filtered_flights.columns:
        #print(col)
        headers.append(col)
    headers[0] = 'Index'
    headerindex = 0

    for i in headers:
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 8),bg = 'lightgrey',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1
    #df2.to_csv('headless.csv', header=False, index=False)
    listedDF = filtered_flights.values.tolist()
    i_index = 2
    j_index = 0

    for i in listedDF:
        for j in i:
            tk.Label(p3frame.interior, text=j,font=("Helvetica", 12),bg = 'white',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            j_index +=1
        i_index +=1
        j_index = 0
#    tk.Button(page3, text="More...", font=('helvetica', 12), command=lambda: moreGrafix).grid(row=2, column=0)
    tk.Button(page3b,text="Refresh", font=('helvetica', 12), command=lambda: p3brefresh(page3b)).grid(row=0,column=1, sticky="E")
    tk.Button(page3b, text="Back", font=('helvetica', 12), command=lambda: p3bclose(page3b)).grid(row=3, column=0, sticky="W")

#    # create a vertical scrollbar for scrolling it
#    vscrollbar = tk.Scrollbar(page3)
#    vscrollbar.grid(row=1, column=2)
#
#    p3canvas = tk.Canvas(page3, width=1600, height=700, yscrollcommand=vscrollbar.set)
#    p3canvas.grid(row=2, column=1, columnspan=4)
#
#    p3frame = tk.Frame(page3)
#    p3frame.grid()
#
#    interior_id = p3canvas.create_window(1000, 1000, window=p3frame, anchor="nw")
#    p3canvas.itemconfigure(interior_id)
#
##    vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
#
#
##    p3canvas.create_window(width=1600, height=800, window=page3)
#
##    p3table2 = tk.Canvas(p3canvas, width=1400, height=700)
##    p3table2.grid(row=2, column=1, columnspan=4)
#
##    scrollbar = tk.Scrollbar(p3canvas)
#
#    ###colortester code###
#
#    day=[1]
#    desk=[3]
#
#    df= pd.read_csv('sep_2019 MELT.csv')
#
#    global df2
#
#    desk_new=[] #list for new desks
#    for i in desk:
#        desk_new.append(str(i))
#
#    df1= df[df.Day.isin(day)]   #list of days in file
#    df2= df1[df1.Desk.isin(desk_new)]  #needs to be a string
#
##    layout = tabulate(df2)
#
#    headers = []
#
#    for col in df2.columns:
#        headers.append(col)
#
##    headers[0] = 'Desk#'
##    headerindex = 0
#
##    for i in headers:
##        tk.Label(canvas1, text=i,font=("Helvetica", 16),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 0, column = headerindex, sticky = 'w'+'e')
##        headerindex +=1
#
##    listedDF = df2.values.tolist()  #list of df
##    i_index = 1
##    j_index = 0
#
#    #makes green and orange labels onto the grid if over/under 100
##    for i in listedDF:
##        for j in i:
##            if i[0] < 101:
##                tk.Label(canvas1, text=j,font=("Helvetica", 16),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
##            else:
##                tk.Label(canvas1, text=j,font=("Helvetica", 16),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
##            j_index +=1
##        i_index +=1
##        j_index = 0
#
##    scrollbar.grid(row=1, column=5, sticky="N"+"S")
##    scrollbar.config(command=p3table.yview)
#
#    ###colortester code end###
#
#    tk.Label(page3, text="Desk #").grid(row=1, column=1, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Releases/hr").grid(row=1, column=2, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Flights/hr").grid(row=1, column=3, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Stations/hr").grid(row=1, column=4, sticky="W"+"E")
#
##    listbox1 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
##    for i in range(1000):
##        listbox1.insert(tk.END, str(i))
##    listbox1.grid(row=1, column=0, sticky="N"+"S")
##
##    listbox2 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
##    for i in range(1000):
##        listbox2.insert(tk.END, str(i))
##    listbox2.grid(row=1, column=1, sticky="N"+"S")
##
##    listbox3 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
##    for i in range(1000):
##        listbox3.insert(tk.END, str(i))
##    listbox3.grid(row=1, column=2, sticky="N"+"S")
##
##    listbox4 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
##    for i in range(1000):
##        listbox4.insert(tk.END, str(i))
##    listbox4.grid(row=1, column=3, sticky="N"+"S")
#
#    tk.Button(page3, text="More...", font=('helvetica', 12), command=lambda: moreGrafix).grid(row=2, column=0)
#    tk.Button(page3,text="Refresh", font=('helvetica', 12), command=lambda: p3refresh(page3)).grid(row=0,column=4, sticky="W"+"E")
#    tk.Button(page3, text="Back", font=('helvetica', 12), command=lambda: p3close(page3)).grid(row=3, column=0)

#def checkday(day):
#    try:
#        int(day)
#    except:
#        tk.messagebox.showerror('Error', 'Please enter an integer for day of the month')
#    if int(day)<=0 or int(day)>31:
#        tk.messagebox.showerror('Error', 'Please enter a valid number for day of the month')
#
#
#def checkhour(hour):
#    try:
#        int(hour)
#    except:
#        tk.messagebox.showerror('Error', 'Please enter an integer for hour')
#    if int(hour)<0 or int(hour)>23:
#        tk.messagebox.showerror('Error', 'Please enter a valid number for hour')

#canvas1 = tk.Canvas(root, width = 400, height = 400, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.grid()


##############
###Filters ###
##############
def flight_filter(df, org,dest,day_,hour_):
    day=[]
    hour=[]
    for d in day_:
        day.append(np.int64(d))
    for h in hour_:
        hour.append(np.int64(h))

    #print(dest,len(dest))
#     return(len(org),len(dest),len(day),len(hour))
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)>0:  #no org

        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
#         return(type(df['Org'][0]),type(df['Dst'][0]),type(df['Day'][1])==numpy.int64,type(df['RlsHR'][1])==numpy.int64)
        return fl3


    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no dest
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3

    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        return fl3

    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no org,dest
        fl1=df[df.Day.isin(day)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no org,day
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no org,hour
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #no dest,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2
    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #no dest,day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #no day,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #only org
        fl1=df[df.Org.isin(org)]
        return fl1
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #only dest
        fl1=df[df.Dst.isin(dest)]
        return fl1
    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #only day
        fl1=df[df.Day.isin(day)]
        return fl1
    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #only hour
        fl1=df[df.Rls_HR.isin(hour)]
        return fl1

    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #none entered
        return df
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)>0:
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        fl4=fl3[fl3.Rls_HR.isin(hour)]
        return fl4
def desk_filter(df, date, desk):
    '''
    Def: Filters desk by desk names and day
    Inputs:
        df: full melted dataframe
        day: datetime element YYYY-MM-DD (as strings)
        desk: list of desks to pull (as strings)
    Return: new dataframe with filtered flights by desk and date
    '''

    df_date = df.loc[df['Date'] == date]
    df_date_desk = df_date[df_date['Desk'].isin(desk)]

    return df_date_desk


def event_hours(df):
    '''
    Def: Generates dataframe of flight events each hour for one desk
    Inputs:
        df: desk_filter dataframe
    Return: new dataframe fl_id indexes, columns for each hour,
        and what event happens in each hour (rls, dep, mon, arr)
    '''

    events = pd.DataFrame(columns = [i for i in range(0, 24)] + ['Desk'])

    for i in range(len(df)):

        #get row from df
        row = df.iloc[i]

        # get event hours
        rls_hr = row['Rls_HR']
        dep_hr = row['Dept_HR']
        arr_hr = row['Arr_HR']
        mon_hrs = [hr for hr in range(dep_hr + 1, arr_hr)]

        # hours 0 to 23
        hours_list = [0 for num in range(0, 24)]

        # insert event into event hours list at specified hour
        hours_list[rls_hr] = 'R'
        hours_list[dep_hr] = 'D'
        hours_list[arr_hr] = 'A'
        for hr in mon_hrs:
            hours_list[hr] = 'M'

        # pull unique flight ID
        fl_ID = df.iloc[i]['FltID']

        # insert events into event hours dataframe for specified flight
        events.loc[fl_ID] = hours_list + [df.iloc[i]['Desk']]

    return events

def max_rls(event_hours):

    '''
    Def: Counts releases per hour and outputs max rls and hour it happens
    Inputs:
        df: event_hours df
    Return: max release at desk and hour it happens
    '''

    num_rls = pd.Series()

    hrs = [i for i in range(0, 24)]

    for hr in hrs:
        counts = event_hours[hr].value_counts()

        if 'R' in counts:
            counts_R = counts['R']
        else:
            counts_R = 0

        num_rls.loc[hr] = counts_R

    # max value and hour it's at
    max_rls = max(num_rls)
    argmax = num_rls.idxmax(axis = 1)

    return str(max_rls) + ' at hour ' + str(argmax) #not a tuple; will need work on this part

def max_flights(event_hours):

    '''
    Def: Counts flights per hour (R, D, M, A) and outputs max flights and hour it happens
    Inputs:
        df: event_hours df
    Return: max flights at desk and hour it happens
    '''

    num_flights = pd.Series()

    hrs = [i for i in range(0, 24)]

    for hr in hrs:

        counts = event_hours[hr].value_counts()

        counts_0 = counts[0]

        num_flights.loc[hr] = counts_0

    # max value and hour it's at
    max_flights = max(num_flights)
    argmax = num_flights.idxmax(axis = 1)

    return str(max_flights) + ' at hour ' + str(argmax) #not a tuple; will need work on this part

def max_cities(df):
    '''
    Def: Counts cities per hour over course of desk
    Inputs:
        df: day_filter df
    Return: list of tuples with first value desk, second value max number of cities on desk
    '''
    city_constraint = np.full((24,1),10)
    org_cities = df.filter(['Org','Desk','Rls_HR','Dept_HR','Arr_HR'])
    org_Rls_cities = org_cities.filter(['Org','Desk','Rls_HR']).rename(columns={"Org": "City"})
    org_Dept_cities = org_cities.filter(['Org','Desk','Dept_HR']).rename(columns={"Org": "City"})
    org_Arr_cities = org_cities.filter(['Org','Desk','Arr_HR']).rename(columns={"Org": "City"})


    dst_cities = df.filter(['Dst','Desk','Rls_HR','Dept_HR','Arr_HR'])
    dst_Rls_cities = dst_cities.filter(['Dst','Desk','Rls_HR']).rename(columns={"Dst": "City"})
    dst_Dept_cities = dst_cities.filter(['Org','Desk','Dept_HR']).rename(columns={"Dst": "City"})
    dst_Arr_cities = dst_cities.filter(['Org','Desk','Arr_HR']).rename(columns={"Dst": "City"})

    cities = org_Rls_cities.append([dst_Rls_cities,org_Dept_cities,dst_Dept_cities,org_Arr_cities,dst_Arr_cities]).groupby(['Desk','Rls_HR']).nunique()
    cities = cities.filter(['City'])

    cities_max_list = []
    for desk in cities.groupby(level=0):
        hrs = pd.DataFrame([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],columns=['Hours']).astype(int)
        desk_subset = desk[1].merge(hrs, how= 'right',left_on ='Rls_HR' , right_on='Hours').fillna(0)
        desk_subset = desk_subset.sort_values(by= 'Hours')
        num_cities = [int(i) for i in desk_subset['City']]
        max_hour = desk[1].idxmax(axis=0)[0][1]

    return str(max(num_cities)) + ' at hour ' + str(int(max_hour)) #not a tuple; will need work on this part

def desk_display(df, date, desks):
    '''
    Def: Filters desk by desk names and day and calculates capacity metrics
    Inputs:
        df: full melted dataframe
        day: datetime element YYYY-MM-DD (as strings)
        desk: list of desks to pull (as strings)
    Return: new dataframe with filtered desks and metrics
    '''

    filtered_desks_df = desk_filter(melt, date, desks)

    desk_display_df = pd.DataFrame(columns = ['Max Releases', 'Max Flights', 'Max Cities'])
    for desk in desks:
        desk_subset = filtered_desks_df.loc[filtered_desks_df['Desk'] == desk]
        events = event_hours(desk_subset)
        rls = max_rls(events)
        flights = max_flights(events)
        stations = max_cities(desk_subset)
        desk_display_df.loc[str(desk)] = [rls,flights,stations]

    return desk_display_df


def workload_dist(desk, window):
    '''
    Def: Graphs workload distribution over course of desk
    Inputs:
        desk number: desk to graph
    Return: plot of workload distribution with conditional coloring
    '''

    # pull data for that desk from desk filter

    desk_data = desk_filter(desk_filter_data, date, [desk])

    # create event hours for desk_data

    events = event_hours(desk_data)

    # lower bound on times to do each task
    rls_time = 5
    dep_time = 1
    arr_time = 3
    mon_time = 2

    # events for that flight
    hrs = list((events.columns))[0:-1]
    time_worked = []

    # flight event list to input in dataframe
    for hr in hrs:
        counts = events[hr].value_counts()

        if 'A' in counts:
            counts_A = counts['A']
        else:
            counts_A = 0

        if 'R' in counts:
            counts_R = counts['R']
        else:
            counts_R = 0

        if 'D' in counts:
            counts_D = counts['D']
        else:
            counts_D = 0

        if 'M' in counts:
            counts_M = counts['M']
        else:
            counts_M = 0

        total_time = rls_time*counts_R + dep_time*counts_D + arr_time*counts_A + mon_time*counts_M
        time_worked.append(total_time)

    # graph line color conditional on capacity
    for time in time_worked:
        if time > 60:
            color = 'red'
            break
        else:
            color = 'green'

    figure1 = plt.Figure(figsize=(6,5), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, window)
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    #hrs.plot()(kind='bar', legend=True, ax=ax1, color = color)
    ax1.plot(hrs, time_worked, color = color) # workload plot
    ax1.plot(hrs, [60 for i in range(24)], color = 'blue') # capacity plot
    ax1.set_title('Workload Distribution')
    plt.show()

    return plt

def releases_dist(desk, window):
    '''
    Def: Graphs releases per hour over course of desk
    Inputs:
        event_hours: event_hours df
    Return: plot of releases per hour with conditional coloring
    '''

    # pull data for that desk from desk filter

    desk_data = desk_filter(desk_filter_data, date, [desk])

    # create event hours for desk_data

    events = event_hours(desk_data)

    num_rls = []

    hrs = list((events.columns))[0:-1]

    for hr in hrs:

        counts = events[hr].value_counts()

        if 'R' in counts:
            counts_R = counts['R']
        else:
            counts_R = 0

        num_rls.append(counts_R)

    for num in num_rls:
        if num > 10:
            color = 'red'
            break
        else:
            color = 'green'
    figure2 = plt.Figure(figsize=(6,5), dpi=100)
    ax2 = figure2.add_subplot(111)
    bar2 = FigureCanvasTkAgg(figure2, window)
    bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax2.plot(hrs, num_rls, color = color)
    ax2.plot(hrs, [10 for i in range(24)], color = 'blue')
    ax2.set_title('Release Distribution')
    plt.show()

    return plt

def cities_dist(df, window):
    '''
    Def: Graphs cities per hour over course of desk
    Inputs:
        df: desk_filter df
    Return: plot of cities per hour with conditional coloring
    '''
    desk = 'M87'
    df = desk_filter(desk_filter_data, date, [desk])
    org_cities = df.filter(['Org','Desk','Rls_HR','Dept_HR','Arr_HR'])
    org_Rls_cities = org_cities.filter(['Org','Desk','Rls_HR']).rename(columns={"Org": "City"})
    org_Dept_cities = org_cities.filter(['Org','Desk','Dept_HR']).rename(columns={"Org": "City"})
    org_Arr_cities = org_cities.filter(['Org','Desk','Arr_HR']).rename(columns={"Org": "City"})

    dst_cities = df.filter(['Dst','Desk','Rls_HR','Dept_HR','Arr_HR'])
    dst_Rls_cities = dst_cities.filter(['Dst','Desk','Rls_HR']).rename(columns={"Dst": "City"})
    dst_Dept_cities = dst_cities.filter(['Org','Desk','Dept_HR']).rename(columns={"Dst": "City"})
    dst_Arr_cities = dst_cities.filter(['Org','Desk','Arr_HR']).rename(columns={"Dst": "City"})

    cities = org_Rls_cities.append([dst_Rls_cities,org_Dept_cities,dst_Dept_cities,org_Arr_cities,dst_Arr_cities]).groupby(['Desk','Rls_HR']).nunique()
    cities = cities.filter(['City'])
    cities = cities.droplevel('Desk')
    hrs = pd.DataFrame([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],columns=['Hours'])
    cities = cities.merge(hrs, how= 'right',left_on ='Rls_HR' , right_on='Hours').fillna(0)
    cities = cities.sort_values(by= 'Hours')
    num_cities = cities['City'].tolist()

    if all((x <= 10 for x in num_cities)) == True:
        city_color = 'green'
    else:
        city_color = 'red'

    figure3 = plt.Figure(figsize=(6,5), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax4 = figure3.add_subplot(111)
    bar3 = FigureCanvasTkAgg(figure3, window)
    bar3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ###needs to be worked on
    #print(cities)
    rects1 = cities.plot.bar(x='Hours', y='City', color = city_color, ax=ax3)
    ax4.plot(hrs, [10 for i in range(24)], color = 'blue')
    ax4.set_title('Cities Distribution')
    plt.show()

    return plt
##############
###Filters ###
##############



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
