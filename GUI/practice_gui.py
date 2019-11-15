
import pandas as pd
from pandas import DataFrame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import random


def melt_file():

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

    # pops up file browse
    file = filedialog.askopenfilename()

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
    melt['Month'] =  9
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

    searchbar.delete(0, tk.END)
    searchbar.insert(0, file)

    filePath.set(file)

    global xl
    xl = pd.ExcelFile(file)

    return melt

def flight_filter(df, org, dest, day, hour, desk):

    '''
    Def: filters flights by origin, destination, day, and hour
    inputs:
        df: melted data frame
        origin: list of strings
        destination: list of strings
        day: list of integers
        hour: list of integers
    Description: it checks whether there is an empty input(s)
    Return:new dataframe with filtered flights by origin,destination,day, and hour
    '''

    day=[int(d) for d in day]
    hour=[int(h) for h in hour]

    if org == []:
        org = ['ABE', 'ABQ', 'AGS', 'ALB', 'ATL', 'ATW', 'AUS', 'AVL', 'AVP', 'BDL', 'BGR', 'BHM', 'BIL', 'BIS', 'BNA', 'BOI', 'BOS', 'BTR', 'BTV', 'BUF', 'BUR', 'BWI', 'BZN', 'CAE', 'CAK', 'CHA', 'CHO', 'CHS', 'CID', 'CLE', 'CLT', 'CMH', 'COS', 'CRW', 'CVG', 'DAB', 'DAL', 'DAY', 'DCA', 'DEN', 'DFW', 'DSM', 'DTW', 'ECP', 'EGE', 'ELP', 'EVV', 'EWR', 'EYW', 'FAR', 'FAY', 'FCA', 'FLL', 'FNT', 'FSD', 'GEG', 'GNV', 'GPT', 'GRB', 'GRR', 'GSO', 'GSP', 'GTF', 'HDN', 'HOU', 'HPN', 'HSV', 'IAD', 'IAH', 'ICT', 'ILM', 'IND', 'JAC', 'JAN', 'JAX', 'JFK', 'LAS', 'LAX', 'LEX', 'LFT', 'LGA', 'LGB', 'LIT', 'MCI', 'MCO', 'MDT', 'MDW', 'MEM', 'MHT', 'MIA', 'MKE', 'MLB', 'MOB', 'MSN', 'MSO', 'MSP', 'MSY', 'MTJ', 'MYR', 'OAK', 'OKC', 'OMA', 'ONT', 'ORD', 'ORF', 'PBI', 'PDX', 'PHF', 'PHL', 'PHX', 'PIT', 'PNS', 'PSC', 'PSP', 'PVD', 'PWM', 'RAP', 'RDU', 'RIC', 'RNO', 'ROA', 'ROC', 'RSW', 'SAN', 'SAT', 'SAV', 'SBN', 'SDF', 'SEA', 'SFO', 'SJC', 'SLC', 'SMF', 'SNA', 'SRQ', 'STL', 'SYR', 'TLH', 'TPA', 'TRI', 'TUL', 'TUS', 'TVC', 'TYS', 'VPS', 'XNA', 'YEG', 'YUL', 'YVR', 'YWG', 'YXE', 'YYC', 'YYZ']

    if dest == []:
        dest = ['ABE', 'ABQ', 'AGS', 'ALB', 'ATL', 'ATW', 'AUS', 'AVL', 'AVP', 'BDL', 'BGR', 'BHM', 'BIL', 'BIS', 'BNA', 'BOI', 'BOS', 'BTR', 'BTV', 'BUF', 'BUR', 'BWI', 'BZN', 'CAE', 'CAK', 'CHA', 'CHO', 'CHS', 'CID', 'CLE', 'CLT', 'CMH', 'COS', 'CRW', 'CVG', 'DAB', 'DAL', 'DAY', 'DCA', 'DEN', 'DFW', 'DSM', 'DTW', 'ECP', 'EGE', 'ELP', 'EVV', 'EWR', 'EYW', 'FAR', 'FAY', 'FCA', 'FLL', 'FNT', 'FSD', 'GEG', 'GNV', 'GPT', 'GRB', 'GRR', 'GSO', 'GSP', 'GTF', 'HDN', 'HOU', 'HPN', 'HSV', 'IAD', 'IAH', 'ICT', 'ILM', 'IND', 'JAC', 'JAN', 'JAX', 'JFK', 'LAS', 'LAX', 'LEX', 'LFT', 'LGA', 'LGB', 'LIT', 'MCI', 'MCO', 'MDT', 'MDW', 'MEM', 'MHT', 'MIA', 'MKE', 'MLB', 'MOB', 'MSN', 'MSO', 'MSP', 'MSY', 'MTJ', 'MYR', 'OAK', 'OKC', 'OMA', 'ONT', 'ORD', 'ORF', 'PBI', 'PDX', 'PHF', 'PHL', 'PHX', 'PIT', 'PNS', 'PSC', 'PSP', 'PVD', 'PWM', 'RAP', 'RDU', 'RIC', 'RNO', 'ROA', 'ROC', 'RSW', 'SAN', 'SAT', 'SAV', 'SBN', 'SDF', 'SEA', 'SFO', 'SJC', 'SLC', 'SMF', 'SNA', 'SRQ', 'STL', 'SYR', 'TLH', 'TPA', 'TRI', 'TUL', 'TUS', 'TVC', 'TYS', 'VPS', 'XNA', 'YEG', 'YUL', 'YVR', 'YWG', 'YXE', 'YYC', 'YYZ']


    fl1 = df[df.Org.isin(org)]
    fl2 = fl1[fl1.Dst.isin(dest)]
    fl3 = fl2[fl2.Day.isin(day)]
    fl4 = fl3[fl3.Rls_HR.isin(hour)]
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

    if date == []:
        date = list(set(list(df['Date'])))

    if desk == []:
        desk = list(set(list(df['Desk'])))

    df_date = df.loc[df['Date'].isin(date)]
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

    return str(max_rls) + ' at hour ' + str(argmax)

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

    return str(max_flights) + ' at hour ' + str(argmax)

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
    return str(max(num_cities)) + ' at hour ' + str(int(max_hour))

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

def workload_dist(desk):
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

    plt.plot(hrs, time_worked, color = color) # workload plot
    plt.plot(hrs, [60 for i in range(24)], color = 'blue') # capacity plot
    plt.show()

def releases_dist(desk):
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

    plt.plot(hrs, num_rls, color = color)
    plt.plot(hrs, [10 for i in range(24)], color = 'blue')
    plt.show()

def cities_dist(df):
    '''
    Def: Graphs cities per hour over course of desk
    Inputs:
        df: desk_filter df
    Return: plot of cities per hour with conditional coloring
    '''
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

    cities.plot.bar(x='Hours', y='City', color = city_color)
    plt.plot(hrs,[10 for i in range(24)], color='blue')
    plt.show()

def verifysheet():

    is_verified = False #by default, this is false until a valid sheet name is given

    for i in xl.sheet_names: #checks for validity of the entry for sheet name given in page 1
        if i==sheetname.get():
            is_verified = True

    if is_verified == False:
        tk.messagebox.showerror('Error', 'Please enter a valid sheetname')  #error message popup window if the given sheet name doesn't match the ones in the excel file

#### [PAGE 2 LEFT] Next button functions. Variables are desk, day1 corresponding to p1 and p2, input as lists
#### p2aCategories, deskList, and dayList are global
def savep2dskInfo(page, p1, p2):
    p2aCategories = []  #refreshes the lsit so it's cleared each time the button is pressed
    p2aCategories.append(p1)    #Adds the Desks and Days that are given by the entry boxes in Page 2
    p2aCategories.append(p2)    #These are for storing the general lists, not for manipulation
    print(p2aCategories)

    deskList = []
    day1List = []

    deskList = list(p1.split(",")) #splits the input from Page 2 by commas for easier
    day1List = list(p2.split(","))

    try:    #Will turn the entry into a proper set of strings into a list
        day1List = list(map(int, day1List))

    except: #Planning on turning this into the defaulting function where all datapoints are selected if the entries are left blank
        print()

    print(deskList, day1List)
    page.destroy() #Closes Page 2
    makeP3a() #Opens Page 3, see makeP3a below

#### [PAGE 2] Window, entries, labels, and buttons
def makeP2():
    ###Page 2a and 2b code###
    page2b=tk.Toplevel()    #Window for Page 2, called "Desks & Flights"
    page2b.title("Desks & Flights")

    page2b.geometry('%dx%d+%d+%d' % (880, 200, 500, 200))   #layers Page 2 over Page 1, sets size

    #variables for the entries in 2b, basically what you'd type in to search in the desk and flight fields
    p2desk = tk.StringVar(page2b)
    p2day1 = tk.StringVar(page2b)
    p2orig = tk.StringVar(page2b)
    p2dest = tk.StringVar(page2b)
    p2day2 = tk.StringVar(page2b)
    p2hour = tk.StringVar(page2b)

    #stores a value for if the All boxes are ticked. 1 is True, 0 is False. Will rework into selecting all the information by default
    #origAll = tk.IntVar()
    #destAll = tk.IntVar()
    #day2All = tk.IntVar()
    #hourAll = tk.IntVar()

    ###Page 2a (LEFT side) code###
    tk.Label(page2b, text = 'Desks',font=('helvetica', 16)).grid(row=0, column=0, columnspan = 3, sticky="W"+"E") #Header for Desks

    #label for Desk on left side, saves the entry variable into p2desk
    tk.Label(page2b, text = 'Desk',font=('helvetica', 14)).grid(row=1, column=0, sticky="W")
    entryDesk = tk.Entry(page2b, textvariable = p2desk, width=50)
    entryDesk.grid(row=1, column=1, columnspan=2)

    #label for Day on left side, saves the entry variable into p2day1
    tk.Label(page2b, text = 'Day',font=('helvetica', 14)).grid(row=2, column=0, sticky="W")
    entry_day = tk.Entry(page2b, textvariable = p2day1, width=50)
    entry_day.grid(row=2, column=1, columnspan=2)

    #Next button, for the left side, goes to Page 3a after going through savep2dskInfo
    p2Nextdsk = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2dskInfo(page2b, p2desk.get(), p2day1.get()))
    p2Nextdsk.grid(row=3, column=1, sticky="W"+"E")

    ###Page 2b (RIGHT side) code end###
    #Flights label, pair on the right side of Desks with column span of 3 instead of 2
    #to accommodate the "All" checkboxes
    tk.Label(page2b, text="Flights",font=('helvetica', 16)).grid(row=0, column=3, columnspan=4, sticky="W"+"E") #Header for Flights

    #Origin, saves entry variable in p2orig
    tk.Label(page2b, text="Origin",font=('helvetica', 14)).grid(row=1, column=3, sticky="W")
    entryOrig = tk.Entry(page2b, textvariable = p2orig, width=50)
    entryOrig.grid(row=1, column=4, columnspan=2)

    #Destination, saves entry variable in p2dest
    tk.Label(page2b, text="Destination",font=('helvetica', 14)).grid(row=2, column=3, sticky="W")
    entryDest = tk.Entry(page2b, textvariable = p2dest, width=50)
    entryDest.grid(row=2, column=4, columnspan=2)

    #Day, int, saves entry variable in p2day2
    tk.Label(page2b, text="Day",font=('helvetica', 14)).grid(row=3, column=3, sticky="W")
    entryDay2 = tk.Entry(page2b, textvariable = p2day2, width=50)
    entryDay2.grid(row=3, column=4, columnspan=2)

    #Hour, string, saves entry variable in p2hour
    tk.Label(page2b, text="Hour",font=('helvetica', 14)).grid(row=4, column=3, sticky="W")
    entryHour = tk.Entry(page2b, textvariable = p2hour, width=50)
    entryHour.grid(row=4, column=4, columnspan=2)

    #Back button, closes Page 2 if clicked
    tk.Button(page2b, text="Back",font=('helvetica', 12), command=lambda: page2b.destroy()).grid(row=5, column=0, sticky="W"+"E")

    #Next button for Flights, calls savep2fltInfo above
    p2Nextflt = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2fltInfo(page2b, p2orig.get(), p2dest.get(), p2day2.get(), p2hour.get()))
    p2Nextflt.grid(row=5, column=4, sticky="W"+"E") #Next button for flights (right side)
#### Page 2b code end ####

#### [PAGE 2 FLIGHT] saves the information on page 2 for Flight side, then closes the window and moves onto page 3b, similar to above function for Desk and page 3a
#### Mostly the same comments as savep2dskInfo above, but with origin, destination, day2, and hour variables instead
def savep2fltInfo(page, p3, p4, p5, p6):
    p2bCategories = []
    p2bCategories.append(p3)
    p2bCategories.append(p4)
    p2bCategories.append(p5)
    p2bCategories.append(p6)
    print(p2bCategories)

    origList = []
    destList = []
    day2List = []
    hourList = []

    origList = list(p3.split(","))
    destList = list(p4.split(","))
    day2List = list(p5.split(","))
    hourList = list(p6.split(","))

    try:
        day2List = list(map(int, day2List))

    except:
        print()

    print(origList, destList, day2List, hourList)

    page.destroy()
    makeP3b()

def p3aclose(p3):   # [PAGE 3a] Back button for Page 3a (DESK), closes the window and calls makeP2 to open Page 2
    p3.destroy()
    makeP2()

def p3bclose(p3):   # [PAGE 3b] Back button for Page 3b (FLIGHT), closes the window and calls makeP2 to open Page 2
    p3.destroy()
    makeP2()

def p3arefresh(p3):   # [PAGE 3a] Back button for Page 3a (DESK), closes the window and opens it again
    p3.destroy()
    makeP3a()

def p3brefresh(p3):   # [PAGE 3b] Back button for Page 3b (FLIGHT), closes the window and opens it again
    p3.destroy()
    makeP3b()

### [PAGE 3 DESK] Shows a new window for the Desks connected to Page 2's left side, and Maximum Releases, Flights, and Stations per hour in a table ###
def makeP3a():
    page3a = tk.Toplevel()  #Page 3a window used for this page
    page3a.geometry('%dx%d+%d+%d' % (500, 880, 400, 80))

    p3frame = VerticalScrolledFrame(page3a) #Calls the scrollbar class to fit a scrollbar onto the frame in the middle of the window
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)

    deskNum=tk.StringVar() #variable to store the desk number to be used in the visualization entry box.

    #visualization for graphs, calls the graphdesk function
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0, sticky='e') #Entry box to search for the appropriate desk. Single desk entry only (no lists)
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w')

    headers = [] #list of names for the headers in Page 3, for the columns

    headers = ['Desk#', 'Max. # of Releases/hr', 'Max # of Flights/hr', 'Max # of Stations/hr'] #The header names in a list
    headerindex = 0 #Index for use in showing headers on the frame with a for function

    #Hardcoding random variables; will replace with max_XXX functions in next version
    for x in range(100):
        a = random.randint(1,20)  #random nummbers for workload/releases
        b = random.randint(1,20)  #random nummbers for flights
        c = random.randint(1,10)  #random nummbers for stations/cities

        if a > 10 or b > 10 or c > 5: #Sets the threshold for green and red rows, according to the value of each variable
            tk.Label(p3frame.interior, text=random.randint(1,100), font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=0, sticky='w'+'e')
            tk.Label(p3frame.interior, text=a, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=1, sticky='w'+'e')
            tk.Label(p3frame.interior, text=b, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=2, sticky='w'+'e')
            tk.Label(p3frame.interior, text=c, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=3, sticky='w'+'e')
        else:
            tk.Label(p3frame.interior, text=random.randint(1,100), font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=0, sticky='w'+'e')
            tk.Label(p3frame.interior, text=a, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=1, sticky='w'+'e')
            tk.Label(p3frame.interior, text=b, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=2, sticky='w'+'e')
            tk.Label(p3frame.interior, text=c, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=3, sticky='w'+'e')

    for i in headers:   #Sets header color as cyan and places them at the top of the frame
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 12), bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1

    #puts refresh and back buttons; refresh calls p3arefresh, to close and reopen this window. Back calls p3aclose and closes the current window and go back to page 2
    tk.Button(page3a,text="Refresh", font=('helvetica', 12), command=lambda: p3arefresh(page3a)).grid(row=0,column=1, sticky="E")
    tk.Button(page3a, text="Back", font=('helvetica', 12), command=lambda: p3aclose(page3a)).grid(row=3, column=0, sticky="W")

# [PAGE 3 FLIGHT] Window for Flights page connected to Page 2's right side
def makeP3b():
    page3b = tk.Toplevel()  #the window variable name used for this function
    page3b.geometry('%dx%d+%d+%d' % (1180, 890, 400, 80))   #fixes location and size for the window

    p3frame = VerticalScrolledFrame(page3b) #Calls the scrollbar class to fit a scrollbar onto the frame in the middle of the window
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)
    #self.label = Label(text="Shrink the window to activate the scrollbar.")
    #self.label.grid(row=1, column=0)

    deskNum=tk.StringVar() #variable to store the desk number to be used in the visualization entry box. Single desk entry only (no lists)
    headers = [] #list of names for the headers in Page 3, for the columns
    headers[0] = 'Desk#' #The header names in a list
    headerindex = 0 #Index for use in showing headers on the frame with a for function

    #visualization for graphs, calls the graphdesk function
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0) #Entry box to search for the appropriate desk. Single desk entry only (no lists)
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w'+'e')

    for col in df2.columns: #Takes in the column names directly from the dataframe
        #print(col)
        headers.append(col)

    for i in headers: #puts the headers onto the top of the frame, in cyan color
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 8),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1

    df2.to_csv('headless.csv', header=False, index=False) #fixed to call the headless.csv file by default
    listedDF = df2.values.tolist() #stores the dataframe values from desk_filter
    i_index = 2 #starting indices for the data to be shown, set so that it ignores the headers and goes straight to the data
    j_index = 0

    for i in listedDF: #iterates over the whole dataframe, shows the data in light green if the desk index is 100 or less, and orange otherwise
        for j in i:
            if i[0] < 101:
                tk.Label(p3frame.interior, text=j,font=("Helvetica", 8),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            else:
                tk.Label(p3frame.interior,text=j,font=("Helvetica", 8),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            j_index +=1

        i_index +=1
        j_index = 0

    #refresh and back buttons. Refresh calls p3brefresh, closing and reopening this window; Back calls p3bclose, closing this window and opening Page 3 again.
    tk.Button(page3b,text="Refresh", font=('helvetica', 12), command=lambda: p3brefresh(page3b)).grid(row=0,column=1, sticky="E")
    tk.Button(page3b, text="Back", font=('helvetica', 12), command=lambda: p3bclose(page3b)).grid(row=3, column=0, sticky="W")

#Jake's scrollbar class, takes in Frame, where the scrollbar is used. Vertical scrolling only
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
            canvas = Canvas(self, bd=0, highlightthickness=0, width=2500, height=800, yscrollcommand=vscrollbar.set)#, xscrollcommand=hscrollbar.set)
            canvas.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=W)
            vscrollbar.config(command=canvas.yview)

            # reset the view
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

### [PAGE 3] graphs desks for three fixed graphs taken from the data of sep_2019.xlsx
def graphdesk(desk):
    #placeholder dataframes

    newWindow = tk.Toplevel()   #New popup window for Visualizer
    newWindow.title("Visualizer")

    newWindow.geometry('%dx%d+%d+%d' % (1800, 800, 100, 100))   #Layers the Visualizer window over the others

    ###Jake's 'Graph from Data' code###
    file = 'sep_2019.xlsx' #fixes file name
    date = '09-01-2019'  #fixes date
    desks = ['M87', 1]  #fixes the desk list for all possible desks
    desk_filter_data = desk_filter(melt, date, desks) #calls the desk_filter function and stores the
    desk_display_df = desk_display(melt, date, desks) #calls the desk_display function and stores the returned dataframes

    desk = 'M87' #Fixes desk chosen as M87

    #For showing the three graphs onto the popup
    workload_dist(desk, newWindow)
    releases_dist(desk, newWindow)
    cities_dist(desk_filter_data, newWindow)

root = tk.Tk()

root.title('Upload Schedule')

filePath = tk.StringVar() # [Page 1] variable for file path

###Page 1 labels, boxes, and buttons###
tk.Label(root, text=" Search for File ",font=(12)).grid(row=0, column=0)

# gets file path and displays it in entry box next to browse button
searchbar = tk.Entry(root, text=filePath.get(), width=50)
searchbar.grid(row=0, column=1)

browseButton_CSV = tk.Button(root, text="Browse", command=melt_file, bg='blue', fg='white', font=('helvetica', 12, 'bold')).grid(row=0,column=2, padx=5, sticky="W"+"E")

uploadButton = tk.Button(root, text="Load", bg='red', font=('helvetica', 12, 'bold'), command=makeP2)
uploadButton.grid(row=3, column=1, pady=10, sticky="W"+"E")

tk.Label(root, text='Please specify sheetname').grid(row=2, column=0)
sheetname = tk.StringVar()
sheetbar = tk.Entry(root, textvariable=sheetname, width=50).grid(row=2, column=1)

tk.Button(root, text = 'Verify', command=verifysheet, bg='blue', fg='white', font=('helvetica', 12, 'bold')).grid(row=2, column=2, padx=5, sticky="W"+"E")

root.geometry('%dx%d+%d+%d' % (800, 120, 500, 200))

root.mainloop()
###Page 1 Stuff END###


