import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    df = pd.read_excel(file, sheet_name='All Flights') #CHANGE FILE AND SHEET NAMES

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

melt = melt_file('oct_2019.xlsx')

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

desk_filter = desk_filter(melt, '2019-10-01', [3])

def flight_filter(df, org,dest,day_,hour_):
    '''
    Def: filters flights by origin, destination, day, and hour
    Inputs:
        #df: melted data frame
        #origin: list of strings
        #destination: list of strings
        #day: list of integers
        #hour: list of integers
    Return:new dataframe with filtered flights by origin,destination,day, and hour
    '''

    day=[]
    hour=[]
    for d in day_:
        day.append(np.int64(d))
    for h in hour_:
        hour.append(np.int64(h))


    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)>0:  # no org

        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3


    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)>0:  # no dest
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3

    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)>0:  # no day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3

    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)==0:  # no hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        return fl3

    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)>0:  # no org,dest
        fl1=df[df.Day.isin(day)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2

    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)>0:  # no org,day
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2

    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)==0:  # no org,hour
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)==0:  # no dest,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)>0:  # no dest,day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2

    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)==0:  # no day,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        return fl2

    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)==0:  # only org
        fl1=df[df.Org.isin(org)]
        return fl1

    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)==0:  # only dest
        fl1=df[df.Dst.isin(dest)]
        return fl1

    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)==0:  # only day
        fl1=df[df.Day.isin(day)]
        return fl1

    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)>0:  # only hour
        fl1=df[df.Rls_HR.isin(hour)]
        return fl1

    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)==0:  # none entered
        return df

    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)>0:   # all entered
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        fl4=fl3[fl3.Rls_HR.isin(hour)]
        return fl4

org = ['ATL', 'LGA']
dest = ['ATL', 'LGA']
day = [12, 13, 14]
hour = []

print(flight_filter(melt,org,dest,day,hour))

def event_hours(df):
    '''
    Def: Generates dataframe of flight events each hour
    Inputs:
        df: desk_filter dataframe
    Return: new dataframe fl_id indexes, columns for each hour,
        and what event happens in each hour (rls, dep, mon, arr)
    '''

    event_hours = pd.DataFrame(columns = [i for i in range(0, 24)] + ['Desk'])

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
        event_hours.loc[fl_ID] = hours_list + [df.iloc[i]['Desk']]

    return event_hours

event_hours = event_hours(desk_filter)

def workload_dist(event_hours):
    '''
    Def: Graphs workload distribution over course of desk
    Inputs:
        event_hours: event_hours df
    Return: plot of workload distribution with conditional coloring
    '''

    # lower bound on times to do each task
    rls_time = 5
    dep_time = 1
    arr_time = 3
    mon_time = 2

    # events for that flight
    hrs = list((event_hours.columns))[0:-1]
    time_worked = []

    # flight event list to input in dataframe
    for hr in hrs:
        counts = event_hours[hr].value_counts()

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

workload_dist(event_hours)

def releases_hr(event_hours):
    '''
    Def: Graphs releases per hour over course of desk
    Inputs:
        event_hours: event_hours df
    Return: plot of releases per hour with conditional coloring
    '''

    num_rls = []

    hrs = list((event_hours.columns))[0:-1]

    for hr in hrs:

        counts = event_hours[hr].value_counts()

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

releases_hr(event_hours)








