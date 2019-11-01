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
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import pandas as pd
#import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#importing filters
import csv
import numpy
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
            hscrollbar = Scrollbar(self, orient=HORIZONTAL)
            hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
            canvas = Canvas(self, bd=0, highlightthickness=0,
                            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
            canvas.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=W)
            vscrollbar.config(command=canvas.yview)
            hscrollbar.config(command=canvas.xview)

            # reset the view
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)

            # create a frame inside the canvas which will be scrolled with it
            self.interior = interior = Frame(canvas)
            interior_id = canvas.create_window(0, 0, window=interior,
                                               anchor=NW)

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


if __name__ == "__main__":

    class SampleApp(Tk):


        def __init__(self, *args, **kwargs):
            page3 = tk.Toplevel()

            self.frame = VerticalScrolledFrame(page3)
            self.frame.grid(row=0, column=0)
            #self.label = Label(text="Shrink the window to activate the scrollbar.")
            #self.label.grid(row=1, column=0)
            def graphdesk(desk):
            #print('you are printing imaginary graphs!')

                #placeholder dataframes

                Data1 = {'Country': ['US','CA','GER','UK','FR'],
                        'GDP_Per_Capita': [45000,42000,52000,49000,47000]
                       }

                df1 = DataFrame(Data1, columns= ['Country', 'GDP_Per_Capita'])
                df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()



                Data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
                        'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
                       }

                df2 = DataFrame(Data2,columns=['Year','Unemployment_Rate'])
                df2 = df2[['Year', 'Unemployment_Rate']].groupby('Year').sum()



                Data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
                        'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
                       }

                df3 = DataFrame(Data3,columns=['Interest_Rate','Stock_Index_Price'])

                #placeholder dataframes

                newWindow = tk.Toplevel()

                print(desk)
                figure1 = plt.Figure(figsize=(6,5), dpi=100)
                ax1 = figure1.add_subplot(111)
                bar1 = FigureCanvasTkAgg(figure1, newWindow)
                bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                df1.plot(kind='bar', legend=True, ax=ax1)
                ax1.set_title('Country Vs. GDP Per Capita')


                figure2 = plt.Figure(figsize=(5,4), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, newWindow)
                line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
                ax2.set_title('Year Vs. Unemployment Rate')


                figure3 = plt.Figure(figsize=(5,4), dpi=100)
                ax3 = figure3.add_subplot(111)
                ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
                scatter3 = FigureCanvasTkAgg(figure3, newWindow)
                scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                ax3.legend()
                ax3.set_xlabel('Interest Rate')
                ax3.set_title('Interest Rate Vs. Stock Index Price')

            deskNum=tk.StringVar()
            entry_deskNum = tk.Entry(self.frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0)
            button_graphdesk = tk.Button(self.frame.interior, text = 'Graph the desk!', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w'+'e')
            headers = []
            for col in df2.columns:
                #print(col)
                headers.append(col)
            headers[0] = 'Desk#'
            headerindex = 0
            for i in headers:
                tk.Label(self.frame.interior,text=i,font=("Helvetica", 8),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
                headerindex +=1
            df2.to_csv('headless.csv', header=False, index=False)
            listedDF = df2.values.tolist()
            i_index = 2
            j_index = 0
            for i in listedDF:
                for j in i:
                    if i[0] < 101:
                        tk.Label(self.frame.interior, text=j,font=("Helvetica", 8),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                    else:
                        tk.Label(self.frame.interior,text=j,font=("Helvetica", 8),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                    j_index +=1
                i_index +=1
                j_index = 0



def makeP3():
    #page3.geometry('%dx%d+%d+%d' % (1800, 880, 50, 20))
    #page3 = tk.Toplevel()
    SampleApp()



    #tk.Button(page3, text="More...", font=('helvetica', 12), command=lambda: moreGrafix).grid(row=2, column=0)
    #tk.Button(page3,text="Refresh", font=('helvetica', 12), command=lambda: p3refresh(page3)).grid(row=0,column=4, sticky="W"+"E")
    #tk.Button(page3, text="Back", font=('helvetica', 12), command=lambda: p3close(page3)).grid(row=3, column=0)

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


#desk_filter([1],[3])
#print(df2)







root.geometry('%dx%d+%d+%d' % (460, 70, 500, 200))

root.mainloop()
