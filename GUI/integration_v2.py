
import pandas as pd
from pandas import DataFrame
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import random
from datetime import datetime


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
    global melt

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
    melt['Desk'] = melt['Desk'].astype(str)

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
    Def: Filters melt dataframe by desk names and day
    Inputs:
        df: full melted dataframe
        day: datetime element YYYY-MM-DD (as strings)
        desk: list of desks to pull (as strings)
    Return: new dataframe with filtered flights by desk and date
    '''
    #If date is not selected, select all dates

    if date == []:
        date = list(set(list(df['Date'])))

    #If desk is not selected, select all desks
    if desk == []:
        desk = list(set(list(df['Desk'])))

    #Filter out all dates in selected dates from melt df
    df_date = df[df['Date'].isin(date) == True]

    #Filter out all desks in selected desks from filtered date df
    df_date_desk = df_date[df_date['Desk'].isin(desk) == True]

    return df_date_desk

def event_hours(melt_df, handoff_df, desk_list):
    '''
    Def: Generates dataframe of flight events each hour for one desk
    Inputs:
        df: desk_filter dataframe
    Return: new dataframe fl_id indexes, columns for each hour,
        and what event happens in each hour (rls, dep, mon, arr)
    '''

    events = pd.DataFrame(columns = [i for i in range(0, 24)] + ['Org','Dst','Desk'])

    df = desk_filter(melt_df, date, desk_list)

    for i in desk_list:
        desk = [i]
        short_desk = i
        desk_df = df[df['Desk'] == i]
        if len(str(desk[0])) == 1:
            desk[0] = 'A0' + str(desk[0])
        if desk[0][0] == 'P' and len(desk[0]) == 2:
            desk[0] = desk[0][0] + '0' + desk[0][1]

        handoff_df['Desk_Ind'] = handoff_df['DESK'].str.find(desk[0])
        desk_subset = handoff_df[handoff_df['Desk_Ind'] == 0].values
        start_shift_desk = desk_subset[0][1]
        end_shift_desk = desk_subset[0][2]
        recieve = desk_subset[0][3]

        if recieve[0] == 'A' and recieve[1] == '0':
            recieve_list = recieve[2:]
        elif recieve[0] == 'A':
            recieve_list = recieve[1:]
        else:
            recieve_list = recieve

        transfer = desk_subset[0][4]


        if recieve == '***' or i[0] == 'M':
            total_df = desk_df
            total_df['New_Desk'] = short_desk
            rec_flight_data = []

        else:
            handoff_df['Rec_Ind'] = handoff_df['DESK'].str.find(recieve)
            rec_subset = handoff_df[handoff_df['Rec_Ind'] == 0].values
            start_shift_rec = rec_subset[0][1]
            end_shift_rec = rec_subset[0][2]
            rec_filter_data = desk_filter(melt_df, date,[recieve_list])
            end_shift_rec_hr = end_shift_rec.hour
            rec_flight_data = []
            #AM Desks #Midnight Desks
            if end_shift_rec > start_shift_rec:
                rec_flight_data = rec_filter_data[rec_filter_data['Arr_Time'].dt.time >= end_shift_rec]
                rec_flight_data = rec_flight_data.append(rec_filter_data[rec_filter_data['Arr_Time'].dt.time <= datetime.strptime('06:00:00', '%H:%M:%S').time()])
                rec_flight_data = rec_flight_data.append(rec_filter_data[rec_filter_data['Dept_Time'].dt.time >= end_shift_rec])
                rec_flight_data = rec_flight_data.append(rec_filter_data[rec_filter_data['Rls_Time'].dt.time >= end_shift_rec])
            #PM Desks
            elif end_shift_rec < start_shift_rec:
                rec_flight_data = rec_filter_data[rec_filter_data['Arr_Time'].dt.time >= end_shift_rec]
                rec_flight_data.append(rec_filter_data[rec_filter_data['Dept_Time'].dt.time >= end_shift_rec])
                rec_flight_data.append(rec_filter_data[rec_filter_data['Rls_Time'].dt.time >= end_shift_rec])


            total_df = desk_df.append(rec_flight_data)
            total_df['New_Desk'] = short_desk


        for i in range(len(total_df)):
            flight_desk = [total_df.iloc[i]['Desk']]
            if len(flight_desk[0]) == 1:
                flight_desk[0] = 'A0' + flight_desk[0]
            if flight_desk[0][0] == 'P' and len(flight_desk[0]) == 2:
                flight_desk = [flight_desk[0][0] + '0' + flight_desk[0][1]]

            #get row from df
            row = total_df.iloc[i]

            # get event hours
            rls_hr = row['Rls_HR']
            dep_hr = row['Dept_HR']
            arr_hr = row['Arr_HR']

            rls_time = row['Rls_Time'].time
            dep_time = row['Dept_Time'].time
            arr_time = row['Arr_Time'].time

            # hours 0 to 23
            hours_list = [0 for num in range(0, 24)]

            # insert event into event hours list at specified hour

            #Recieved handoffs remove tasks before shift starts
            if desk != flight_desk:

                #set monitoring hours
                #if arrival is not past 23
                if dep_hr < arr_hr:
                    mon_hrs = [hr for hr in range(dep_hr + 1, arr_hr)]

                #if arrival is past 23, monitor from 0 up to arrival hour
                else:
                    mon_hrs = [hr for hr in range(dep_hr + 1, 24)]
                    mon_hrs.extend([hr for hr in range(0, arr_hr)])

                hours_list[rls_hr] = 'R'
                hours_list[dep_hr] = 'D'
                hours_list[arr_hr] = 'A'
                for hr in mon_hrs:
                    hours_list[hr] = 'M'

                for hr in range(len(hours_list)):
                    #remove hours outside of desk shift
                    #if desk start hr is < end hr, remove all before start and all after end
                    if start_shift_desk.hour < end_shift_desk.hour and hr < start_shift_desk.hour:
                        hours_list[hr] = 0
                    elif start_shift_desk.hour < end_shift_desk.hour and hr > end_shift_desk.hour:
                        hours_list[hr] = 0
                    #if desk start hr is > end hr, remove all after end hr up to start hour
                    elif start_shift_desk.hour > end_shift_desk.hour and hr > end_shift_desk.hour and hr < start_shift_desk.hour:
                        hours_list[hr] = 0

            #On desk, remove transfer handoffs after end of shift
            else:
                if dep_hr < arr_hr:
                    mon_hrs = [hr for hr in range(dep_hr + 1, arr_hr)]
                elif arr_hr < dep_hr:
                    mon_hrs = [hr for hr in range(dep_hr + 1, 24)]
                    mon_hrs.extend([hr for hr in range(0, arr_hr)])

                hours_list[rls_hr] = 'R'
                hours_list[dep_hr] = 'D'
                hours_list[arr_hr] = 'A'
                for hr in mon_hrs:
                    hours_list[hr] = 'M'

                for hr in range(len(hours_list)):
                    #remove hours outside of desk shift
                    #if desk start hr is < end hr, remove all before start and all after end
                    if start_shift_desk.hour < end_shift_desk.hour and hr < start_shift_desk.hour:
                        hours_list[hr] = 0
                    elif start_shift_desk.hour < end_shift_desk.hour and hr > end_shift_desk.hour:
                        hours_list[hr] = 0
                    #if desk start hr is > end hr, remove all after end hr up to start hour
                    elif start_shift_desk.hour > end_shift_desk.hour and hr > end_shift_desk.hour and hr < start_shift_desk.hour:
                        hours_list[hr] = 0

            # pull unique flight ID
            fl_ID = total_df.iloc[i]['FltID'] + total_df.iloc[i]['Desk'] + total_df.iloc[i]['New_Desk']

            # insert events into event hours dataframe for specified flight
            events.loc[fl_ID] = hours_list + [total_df.iloc[i]['Org']] + [total_df.iloc[i]['Dst']] + [total_df.iloc[i]['New_Desk']]

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

        try:
            counts_0 = counts[0]
        except:
            counts_0 = 0

        num_flights.loc[hr] = counts_0

    # max value and hour it's at
    max_flights = max(num_flights)
    argmax = num_flights.idxmax(axis = 1)

    return str(max_flights) + ' at hour ' + str(argmax)

def max_cities(event_hours):
    '''
    Def: Counts cities per hour over course of desk
    Inputs:
        df: day_filter df
    Return: list of tuples with first value desk, second value max number of cities on desk
    '''

    num_cities = pd.Series()

    org_events = event_hours.copy()
    dst_events = event_hours.copy()

    hrs = [i for i in range(0, 24)]

    for hr in hrs:
        for flight in range(len(org_events)):
            if org_events[hr][flight] != 0:
                org_events[hr][flight] = org_events['Org'][flight]
            else:
                org_events[hr][flight] = org_events[hr][flight]
    for hr in hrs:
        for flight in range(len(dst_events)):
            if dst_events[hr][flight] != 0:
                dst_events[hr][flight] = dst_events['Dst'][flight]
            else:
                dst_events[hr][flight] = dst_events[hr][flight]

    all_cities = org_events.append(dst_events).nunique()[:-3] - 1
    print(type(all_cities))
    print(all_cities)
    max_hour = all_cities.idxmax(axis = 1)

    return str(max(all_cities)) + ' at hour ' + str(int(max_hour))

def desk_display(df, date, desks):
    '''
    Def: Filters desk by desk names and day and calculates capacity metrics
    Inputs:
        df: full melted dataframe
        day: datetime element YYYY-MM-DD (as strings)
        desk: list of desks to pull (as strings)
    Return: new dataframe with filtered desks and metrics
    '''

    desk_display_df = pd.DataFrame(columns = ['Max Releases', 'Max Flights', 'Max Cities'])
    for desk in desks:
        print(desk)
        handoff_df = handoff('Sked-SepEq-19a.xlsx', 'Dom Desk Turnover Sep 2019 ')
        events = event_hours(melt,handoff_df,[desk])
        print(events)
        rls = max_rls(events)
        flights = max_flights(events)
        stations = max_cities(events)
        desk_display_df.loc[str(desk)] = [rls,flights,stations]

    return desk_display_df

def workload_dist(desk):
    '''
    Def: Graphs workload distribution over course of desk
    Inputs:
        desk number: desk to graph
    Return: plot of workload distribution with conditional coloring
    '''
    # create event hours for desk_data

    events = event_hours(melt,handoff_df,desk)

    # lower bound on times to do each task
    rls_time = 5
    dep_time = 1
    arr_time = 3
    mon_time = 2

    # events for that flight
    hrs = list((events.columns))[0:-3]
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
    # create event hours for desk_data

    events = event_hours(melt,handoff_df,desk)

    num_rls = []

    hrs = list((events.columns))[0:-3]

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

def cities_dist(desk):
    '''
    Def: Graphs cities per hour over course of desk
    Inputs:
        df: desk_filter df
    Return: plot of cities per hour with conditional coloring
    '''
    events = event_hours(melt,handoff_df,desk)

    num_cities = pd.Series()

    org_events = events.copy()
    dst_events = events.copy()

    hrs = [i for i in range(0, 24)]

    for hr in hrs:
        for flight in range(len(org_events)):
            if org_events[hr][flight] != 0:
                org_events[hr][flight] = org_events['Org'][flight]
            else:
                org_events[hr][flight] = org_events[hr][flight]
        for flight in range(len(dst_events)):
            if dst_events[hr][flight] != 0:
                dst_events[hr][flight] = dst_events['Dst'][flight]
            else:
                dst_events[hr][flight] = dst_events[hr][flight]

    org_counts = org_events[hr].value_counts()
    all_cities = org_events.append(dst_events).nunique()[:-3] - 1

    if all((x <= 12 for x in all_cities)) == True:
        color = 'green'
    else:
        color = 'red'

    all_cities.plot.bar(color = color)
    plt.plot(hrs, [12 for i in range(24)], color = 'blue')
    plt.show()

def handoff(file,sheet):

    '''
    Def:  takes in and reads shift file used for handoffs
    Inputs:
        file: raw schedule Excel file
        sheet: sheet name of handoff file
    Return: dataframe with desks, shift start time, shift end time, recieve from desk, and transfer to desk
    '''
    #Read all three columns of shift sheet
    df = pd.read_excel(file, sheet_name=sheet, names = ['DESK', 'START', 'END', 'Receive From', 'Xfr To'],index_col=None, usecols = "A:E", nrows= 70,dtype=str)
    df2 = pd.read_excel(file, sheet_name=sheet, names = ['DESK', 'START', 'END', 'Receive From', 'Xfr To'],index_col=None, usecols = "G:K", nrows=15,dtype=str)
    midnight_desks = pd.read_excel(file, sheet_name=sheet, names = ['DESK', 'START', 'END', 'Xfr To','Receive From'], index_col=None, usecols = "G:K", skiprows=18, nrows=8,dtype=str)

    #Append AM and PM desks together
    df = df.append(df2).dropna()
    df['DESK'] = df['DESK'].str.slice(stop=3)
    for i in df['DESK']:
        if i[0] == 'A':
            i = i[1:]

    #Switch Xfr To and Receive From columns to match AM/PM Desks
    midnight_desks = midnight_desks.filter(['DESK', 'START', 'END', 'Receive From', 'Xfr To'])

    #Append Midnight desks to AM/PM
    df = df.append(midnight_desks)

    gmt_convert = 4 #number of hours between EST and GMT
    #Change start and end times to datetime times
    df['START'] = pd.to_datetime(df['START'].astype(str))
    df['START'] = (df['START'] + pd.Timedelta(hours=gmt_convert)).dt.time
    df['END'] = pd.to_datetime(df['END'].astype(str))
    df['END'] = (df['END'] + pd.Timedelta(hours=gmt_convert)).dt.time
    global handoff_df
    handoff_df = df
    return handoff_df

def verifysheet():

    global shtName
    shtName = sheetname.get()
    is_verified = False
    for i in xl.sheet_names:
        if i==sheetname.get():
            is_verified = True
    if is_verified == False:
        tk.messagebox.showerror('Error', 'Please enter a valid sheetname')

#### [PAGE 2 LEFT] Next button functions. Variables are desk, day1 corresponding to p1 and p2, input as lists
#### p2aCategories, deskList, and dayList are global
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
    makeP3a(deskList, day1List)

#### [PAGE 2] Window, entries, labels, and buttons
def makeP2():
    ###Page 2a and 2b code###
    page2b=tk.Toplevel()
    page2b.title("Desks & Flights")

    page2b.geometry('%dx%d+%d+%d' % (980, 200, 500, 200))

    #variables for the entries in 2b, basically what you'd type in to search.
    p2desk = tk.StringVar(page2b)
    p2day1 = tk.StringVar(page2b)
    p2orig = tk.StringVar(page2b)
    p2dest = tk.StringVar(page2b)
    p2day2 = tk.StringVar(page2b)
    p2hour = tk.StringVar(page2b)

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

    for orig in origList:
        if len(orig) != 3:
            tk.messagebox.showerror('Error', 'Please enter a valid origin')
    if origList == ['']:
         origList = []
    for dest in destList:
        if len(dest) != 3:
           tk.messagebox.showerror('Error', 'Please enter a valid destination')
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
def makeP3a(deskList, day1List):

    page3a = tk.Toplevel()
    page3a.geometry('%dx%d+%d+%d' % (500, 880, 400, 80))

    p3frame = VerticalScrolledFrame(page3a)
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)
    print(deskList)
    newList = []
    for i in deskList:
        try:
            newList.append(int(i))
        except:
            newList.append(i)
    deskNum=tk.StringVar()
    print(newList)
    print(day1List)
    file = 'sep_2019.xlsx'
    global date
    #date = ['2019-10-01']
    date = day1List
    global desks
    #desks =['M87','M88','P59','P75','P61', 'P77']
    #desks = [1]
    desks = newList
    global desk_filter_data
    desk_filter_data = desk_filter(melt, date, desks)
    global desk_display_df
    desk_display_df = desk_display(melt, date, desks)
    #visualization for graphs
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0, sticky='e')
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w')
    headers = []
    headers.append('Index')
    deskNum=tk.StringVar()
    entry_deskNum = tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0)
    button_graphdesk = tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w'+'e')

    #headers
    headers = ['Desk#', 'Max. # of Releases/hr', 'Max # of Flights/hr', 'Max # of Stations/hr']
    headerindex = 0

    for i in headers:
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 12), bg = 'lightgrey',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1

    listedDF = desk_display_df.reset_index().values.tolist()
    #print(listedDF)
    i_index = 2
    j_index = 0
    for i in listedDF:
        maxRls = int(i[1][0]+i[1][1])
        maxFlt = int(i[2][0]+i[2][1])
        maxSta = int(i[3][0]+i[3][1])
        #print(maxRls)
        #print(maxFlt)
        #print(maxSta)
        tk.Label(p3frame.interior,text=i[0],font=("Helvetica", 16),bg = 'white', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
        j_index +=1
        if j_index == 1:
            if maxRls >= 10:
                tk.Label(p3frame.interior,text=i[1],font=("Helvetica", 16),bg = 'red', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index +=1
            elif maxRls < 8:
                tk.Label(p3frame.interior,text=i[1],font=("Helvetica", 16),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index +=1
            elif 8<= maxRls <10:
                tk.Label(p3frame.interior,text=i[1],font=("Helvetica", 16),bg = 'yellow', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index +=1
        if j_index == 2:
            if maxFlt >= 24:
                tk.Label(p3frame.interior,text=i[2],font=("Helvetica", 16),bg = 'red', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index +=1
            elif maxFlt < 20:
                tk.Label(p3frame.interior,text=i[2],font=("Helvetica", 16),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index +=1
            elif 20 <= maxFlt < 24:
                tk.Label(p3frame.interior,text=i[2],font=("Helvetica", 16),bg = 'yellow', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index +=1
        if j_index == 3:
            if maxSta >= 12:
                tk.Label(p3frame.interior,text=i[3],font=("Helvetica", 16),bg = 'red', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index = 0
            elif maxSta < 10:
                tk.Label(p3frame.interior,text=i[3],font=("Helvetica", 16),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index = 0
            elif 10<= maxSta <12:
                tk.Label(p3frame.interior,text=i[3],font=("Helvetica", 16),bg = 'yellow', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                j_index = 0

        i_index +=1

    tk.Button(page3a,text="Refresh", font=('helvetica', 12), command=lambda: p3arefresh(page3a)).grid(row=0,column=1, sticky="E")
    tk.Button(page3a, text="Back", font=('helvetica', 12), command=lambda: p3aclose(page3a)).grid(row=3, column=0, sticky="W")

# [PAGE 3 FLIGHT] Window for Flights page connected to Page 2's right side
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

    global filtered_flights
    colList = ['Date', 'Flt', 'Org', 'Dst', 'Eqt', 'MILES', 'Dept_Time', 'Arr_Time', 'Rls_Time', 'Desk']
    filtered_flights = flight_filter(df, org,dest,day_,hour_)
    print('flight filter entries',org,dest,day_,hour_)
    filtered_flights = filtered_flights.filter(items = colList)
    print(filtered_flights)
    ###

    for col in filtered_flights.columns:
        #print(col)
        headers.append(col)
    #headers[0] = 'Index'
    headerindex = 0

    for i in headers:
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 16),bg = 'lightgrey',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1
    #df2.to_csv('headless.csv', header=False, index=False)
    listedDF = filtered_flights.values.tolist()
    i_index = 2
    j_index = 0
    for i in listedDF:
        i[1]=int(i[1])
        i[5]=int(i[5])
        i[6]=i[6][11:16]
        i[7]=i[7][11:16]
        i[8]=i[8][11:16]
    for i in listedDF:
        for j in i:
            tk.Label(p3frame.interior, text=j,font=("Helvetica", 16),bg = 'white',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            j_index +=1
        i_index +=1
        j_index = 0

    tk.Button(page3b,text="Refresh", font=('helvetica', 16), command=lambda: p3brefresh(page3b)).grid(row=0,column=1, sticky="E")
    tk.Button(page3b, text="Back", font=('helvetica', 16), command=lambda: p3bclose(page3b)).grid(row=3, column=0, sticky="W")

# scrollbar class, takes in Frame, where the scrollbar is used. Vertical scrolling only
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
    #global desk
    newWindow = tk.Toplevel()
    newWindow.title("Visualizer")

    newWindow.geometry('%dx%d+%d+%d' % (1800, 800, 100, 100))
    print(desk, type(desk))
    try:
        desk = int(desk)
    except:
        return desk
    print(desk, type(desk))
    ###Jake's 'Graph from Data' code###
    file = 'sep_2019.xlsx'

    global melt
    melt = melt_file(file)
    global date
    date = '10-01-2019'
    global desks
    desks = []
    #desks.append(desk)
    desks.append(1)
    global desk_filter_data
    desk_filter_data = desk_filter(melt, date, desks)
    global desk_display_df
    desk_display_df = desk_display(melt, date, desks)
    desk = 1
    workload_dist(desk, newWindow)
    releases_dist(desk, newWindow)
    cities_dist(desk_filter_data, newWindow, desk)


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


