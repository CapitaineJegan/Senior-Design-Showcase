import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = 'sep_2019.xlsx'

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

    return melt

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

def shift_file(file):
    #Create dataframes from Excel
    df = pd.read_excel(file)
    return df

# test for the display for certain date and selected desks
melt = melt_file(file)
# shift = shift_file('deskTimeRanges.xlsx')
date = '09-01-2019'
desks = ['M87', 1]
desk_filter_data = desk_filter(melt, date, desks)
desk_display(melt, date, desks)

# test for the display fof graphs based on one selected desk
desk = 'M87'
workload_dist(desk)
releases_dist(desk)
cities_dist(desk)
