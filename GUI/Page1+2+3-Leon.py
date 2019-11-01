import tkinter as tk
from tkinter import filedialog
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import ntpath #for taking file name only - still working on that.
from tabulate import tabulate

#
#window = tk.Tk()
#window.title('Upload Schedule')
#window.mainloop()

root= tk.Tk()
root.title('Upload Schedule')

filePath = tk.StringVar()
global df
global p2Categories

#global list values for the entries on Page 2
global deskList
global day1List
global origList
global destList
global day2List
global hourList



def getCSV():#for taking the csv files in the first page button
    global melt
    
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
    
#    print(df)
#    print(melt)
#    
#    return melt
    

#Page 2 Next button functions. Order is desk, day1 info is p1, p2, and origin, destination, day2, and hour are p3, p4, p5,and p6
def savep2Info(page, p1, p2, p3, p4, p5, p6):
    p2Categories = []
    p2Categories.append(p1)
    p2Categories.append(p2)
    p2Categories.append(p3)
    p2Categories.append(p4)
    p2Categories.append(p5)
    p2Categories.append(p6)
    print(p2Categories)
    
    deskList = []
    day1List = []
    origList = []
    destList = []
    day2List = []
    hourList = []
    
    deskList = list(p1.split(","))
    day1List = list(p2.split(","))
    origList = list(p3.split(","))
    destList = list(p4.split(","))
    day2List = list(p5.split(","))
    hourList = list(p6.split(","))
    
    try:
        day1List = list(map(int, day1List))
        day2List = list(map(int, day2List))
        
    except:
        print()
    
    print(deskList, day1List, origList, destList, day2List, hourList)
    page.destroy()
    makeP3()

#Page 2 functions
def makeP2():
    ###Page 2a and 2b code###
    page2b=tk.Toplevel()
    page2b.title("Desks & Flights")
    
    page2b.geometry('%dx%d+%d+%d' % (440, 180, 100, 100))
    
    #variables for the entries in 2b, basically what you'd type in to search.
    p2desk = tk.StringVar(page2b)
    p2day1 = tk.StringVar(page2b)
    p2orig = tk.StringVar(page2b)
    p2dest = tk.StringVar(page2b)
    p2day2 = tk.StringVar(page2b)
    p2hour = tk.StringVar(page2b)
    
    #stores a value for if the All boxes are ticked. 1 is True, 0 is False. *Might not need*
    origAll = tk.IntVar()
    destAll = tk.IntVar()
    day2All = tk.IntVar()
    hourAll = tk.IntVar()
    
    ###Page 2a code###
    entryDesk = tk.Entry(page2b, textvariable = p2desk)
    entryDesk.grid(row=1, column=1)
    
    tk.Label(page2b, text = 'Desk',font=('helvetica', 14)).grid(row=1, column=0, sticky="W")
    
#    canvas1 = tk.Canvas(page2b, width = 400, height = 400)
#    canvas1.pack()
#    entry1 = tk.Entry(page2b)
#    entry1.grid(row=1, column=1)
#    tk.Label(page2b, text="Desks", width = 10).grid(row=0, column=0, columnspan=2)
#    tk.Label(page2b, text="Day:", width = 10).grid(row=1, column=0)
    entry_day = tk.Entry(page2b, textvariable = p2day1)
    entry_day.grid(row=2, column=1)
    
    tk.Label(page2b, text = 'Desks',font=('helvetica', 16)).grid(row=0, column=0, columnspan = 2, sticky=tk.W+tk.E)
    tk.Label(page2b, text = 'Day',font=('helvetica', 14)).grid(row=2, column=0, sticky="W")
    ###Page 2a code end### 
    
    #canvas1 = tk.Canvas(root, width=800,height=400).grid()
    #Flights label, pair on the right side of Desks with column span of 3 instead of 2
    #to accommodate the "All" checkboxes
    tk.Label(page2b, text="Flights",font=('helvetica', 16)).grid(row=0, column=2, columnspan=3, sticky="W"+"E")
    
    #Origin
    tk.Label(page2b, text="Origin",font=('helvetica', 14)).grid(row=1, column=2, sticky="W")
    entryOrig = tk.Entry(page2b, textvariable = p2orig)
    entryOrig.grid(row=1, column=3)
    #listbox = tk.OptionMenu(root, orig, 1)
    #listbox.grid(row=1, column=3)
    cOrig = tk.Checkbutton(page2b, text="All", variable=origAll)
    cOrig.grid(row=1, column=4)
    
    #Destination
    tk.Label(page2b, text="Destination",font=('helvetica', 14)).grid(row=2, column=2, sticky="W")
    entryDest = tk.Entry(page2b, textvariable = p2dest)
    entryDest.grid(row=2, column=3)
    #listbox = tk.OptionMenu(root, dest,2,3)
    #listbox.grid(row=2, column=3)
    cDest = tk.Checkbutton(page2b, text="All", variable=destAll)
    cDest.grid(row=2, column=4)
    
    #Day, int
    tk.Label(page2b, text="Day",font=('helvetica', 14)).grid(row=3, column=2, sticky="W")
    entryDay2 = tk.Entry(page2b, textvariable = p2day2)
    entryDay2.grid(row=3, column=3)
    #listbox = tk.OptionMenu(root, day2,2,3)
    #listbox.grid(row=3, column=3)
    cDay = tk.Checkbutton(page2b, text="All", variable=day2All)
    cDay.grid(row=3, column=4)
    
    #Hour, string
    tk.Label(page2b, text="Hour",font=('helvetica', 14)).grid(row=4, column=2, sticky="W")
    entryHour = tk.Entry(page2b, textvariable = p2hour)
    entryHour.grid(row=4, column=3)
    #listbox = tk.OptionMenu(root, hour,2,3)
    #listbox.grid(row=4, column=3)
    cHour = tk.Checkbutton(page2b, text="All", variable=hourAll)
    cHour.grid(row=4, column=4)
    
    tk.Button(page2b, text="Back",font=('helvetica', 12), command=lambda: page2b.destroy()).grid(row=5, column=0, sticky="W"+"E") #Back button
    
    p2Next = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2Info(page2b, p2desk.get(), p2day1.get(), p2orig.get(), p2dest.get(), p2day2.get(), p2hour.get()))
    p2Next.grid(row=5, column=3, columnspan=2, sticky="W"+"E") #Next button
    ###Page 2b code end###

def p3close(p3):
    p3.destroy()
    makeP2()

def moreGrafix():
    
    return 1

def p3refresh(p3):
    p3.destroy()
    makeP3()

#Page 3 functions
def makeP3():
    page3 = tk.Toplevel()
    page3.geometry('%dx%d+%d+%d' % (1800, 880, 50, 20))
    
    # create a vertical scrollbar for scrolling it
    vscrollbar = tk.Scrollbar(page3)
    vscrollbar.grid(row=1, column=2)
    
    p3canvas = tk.Canvas(page3, width=1600, height=700, yscrollcommand=vscrollbar.set)
    p3canvas.grid(row=2, column=1, columnspan=4)
    
    p3frame = tk.Frame(page3)
    p3frame.grid()
    
    interior_id = p3canvas.create_window(1000, 1000, window=p3frame, anchor="nw")
    p3canvas.itemconfigure(interior_id)
    
#    vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
    
    
#    p3canvas.create_window(width=1600, height=800, window=page3)
    
#    p3table2 = tk.Canvas(p3canvas, width=1400, height=700)
#    p3table2.grid(row=2, column=1, columnspan=4)
    
#    scrollbar = tk.Scrollbar(p3canvas)
    
    ###colortester code###
    
    day=[1]
    desk=[3]
    
    df= pd.read_csv('sep_2019 MELT.csv')
    
    global df2
    
    desk_new=[] #list for new desks
    for i in desk:
        desk_new.append(str(i))
    
    df1= df[df.Day.isin(day)]   #list of days in file
    df2= df1[df1.Desk.isin(desk_new)]  #needs to be a string
    
#    layout = tabulate(df2)
    
    headers = []
    
    for col in df2.columns:
        headers.append(col)
    
    headers[0] = 'Desk#'
    headerindex = 0
    
    for i in headers:
        tk.Label(canvas1, text=i,font=("Helvetica", 16),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 0, column = headerindex, sticky = 'w'+'e')
        headerindex +=1
    
    listedDF = df2.values.tolist()  #list of df
    i_index = 1
    j_index = 0
    
    #makes green and orange labels onto the grid if over/under 100
    for i in listedDF:
        for j in i:
            if i[0] < 101:
                tk.Label(canvas1, text=j,font=("Helvetica", 16),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            else:
                tk.Label(canvas1, text=j,font=("Helvetica", 16),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            j_index +=1
        i_index +=1
        j_index = 0
    
#    scrollbar.grid(row=1, column=5, sticky="N"+"S")
#    scrollbar.config(command=p3table.yview)
    
    ###colortester code end###
    
#    tk.Label(page3, text="Desk #").grid(row=1, column=0, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Releases/hr").grid(row=1, column=1, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Flights/hr").grid(row=1, column=2, sticky="W"+"E")
#    tk.Label(page3, text="Max # of Stations/hr").grid(row=1, column=3, sticky="W"+"E")
    
#    listbox1 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
#    for i in range(1000):
#        listbox1.insert(tk.END, str(i))
#    listbox1.grid(row=1, column=0, sticky="N"+"S")
#    
#    listbox2 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
#    for i in range(1000):
#        listbox2.insert(tk.END, str(i))
#    listbox2.grid(row=1, column=1, sticky="N"+"S")
#    
#    listbox3 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
#    for i in range(1000):
#        listbox3.insert(tk.END, str(i))
#    listbox3.grid(row=1, column=2, sticky="N"+"S")
#    
#    listbox4 = tk.Listbox(p3frame, yscrollcommand=scrollbar.set, height=40)
#    for i in range(1000):
#        listbox4.insert(tk.END, str(i))
#    listbox4.grid(row=1, column=3, sticky="N"+"S")
    
    tk.Button(page3, text="More...", font=('helvetica', 12), command=lambda: moreGrafix).grid(row=2, column=0)
    tk.Button(page3,text="Refresh", font=('helvetica', 12), command=lambda: p3refresh(page3)).grid(row=0,column=4, sticky="W"+"E")
    tk.Button(page3, text="Back", font=('helvetica', 12), command=lambda: p3close(page3)).grid(row=3, column=0)

#will incorporate these two checks for accuracy of entries later this week
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
        
canvas1 = tk.Canvas(root, width = 400, height = 400, bg = 'lightsteelblue2', relief = 'raised')
#canvas1.grid()

tk.Label(root, text=" Search for File ",font=(12)).grid(row=0, column=0)

searchbar = tk.Entry(root, text=filePath.get(), width=50)
searchbar.grid(row=0, column=1)

browseButton_CSV = tk.Button(text="Browse", command=getCSV, bg='green', fg='white', font=('helvetica', 12, 'bold')).grid(row=1,column=0, sticky="W"+"E")
canvas1.create_window(200, 200, window=browseButton_CSV)

uploadButton = tk.Button(text="Load",font=('helvetica', 12, 'bold'), command=makeP2)
uploadButton.grid(row=1, column=1, sticky="W"+"E")

root.geometry('%dx%d+%d+%d' % (460, 70, 500, 200))

root.mainloop()