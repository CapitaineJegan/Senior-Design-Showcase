import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from plotnine import *
from plotnine.data import mpg
import matplotlib.pyplot as plt

#Create dataframes from Excel
df = pd.read_excel('oct_2019.xlsx', sheet_name='All Flights') #CHANGE FILE AND SHEET NAMES
# df2 = pd.read_excel('regionMapping.xlsx', sheet_name='regionMapping') #CHANGE FILE AND SHEET NAMES
# df3 = pd.read_excel('regionMapping2.xlsx', sheet_name='regionMapping') #CHANGE FILE AND SHEET NAMES

#Create airport list
aiport_list = ['ABE', 'ABQ', 'AGS', 'ALB', 'ATL', 'ATW', 'AUS', 'AVL', 'AVP', 'BDL', 'BGR', 'BHM', 'BIL', 'BIS', 'BNA', 'BOI', 'BOS', 'BTR', 'BTV', 'BUF', 'BUR', 'BWI', 'BZN', 'CAE', 'CAK', 'CHA', 'CHO', 'CHS', 'CID', 'CLE', 'CLT', 'CMH', 'COS', 'CRW', 'CVG', 'DAB', 'DAL', 'DAY', 'DCA', 'DEN', 'DFW', 'DSM', 'DTW', 'ECP', 'EGE', 'ELP', 'EVV', 'EWR', 'EYW', 'FAR', 'FAY', 'FCA', 'FLL', 'FNT', 'FSD', 'GEG', 'GNV', 'GPT', 'GRB', 'GRR', 'GSO', 'GSP', 'GTF', 'HDN', 'HOU', 'HPN', 'HSV', 'IAD', 'IAH', 'ICT', 'ILM', 'IND', 'JAC', 'JAN', 'JAX', 'JFK', 'LAS', 'LAX', 'LEX', 'LFT', 'LGA', 'LGB', 'LIT', 'MCI', 'MCO', 'MDT', 'MDW', 'MEM', 'MHT', 'MIA', 'MKE', 'MLB', 'MOB', 'MSN', 'MSO', 'MSP', 'MSY', 'MTJ', 'MYR', 'OAK', 'OKC', 'OMA', 'ONT', 'ORD', 'ORF', 'PBI', 'PDX', 'PHF', 'PHL', 'PHX', 'PIT', 'PNS', 'PSC', 'PSP', 'PVD', 'PWM', 'RAP', 'RDU', 'RIC', 'RNO', 'ROA', 'ROC', 'RSW', 'SAN', 'SAT', 'SAV', 'SBN', 'SDF', 'SEA', 'SFO', 'SJC', 'SLC', 'SMF', 'SNA', 'SRQ', 'STL', 'SYR', 'TLH', 'TPA', 'TRI', 'TUL', 'TUS', 'TVC', 'TYS', 'VPS', 'XNA', 'YEG', 'YUL', 'YVR', 'YWG', 'YXE', 'YYC', 'YYZ']
df = df[df['Org'].isin(aiport_list)]
df = df[df['Dst'].isin(aiport_list)]
#Join dataframes to get rid of international flights
# df = df.join(df2.set_index('Station'), on='Org')
# df = df.join(df3.set_index('Station'), on='Dst')
# df = df.dropna(subset=['Orig Region','Dest Region'])

#THIS MELTS DF
melt = pd.melt(df, id_vars=['Flt','Org','Dst','Eqt','Dptr','Arvl','BLK MINS','MILES','Desk'] 
	,value_vars=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
	,var_name = 'Day'
	,value_name = 'Schd')

#Drop not scheduled flights N/A
melt = melt.dropna(subset=['Schd'])

#Set Year, Month and Date
melt['Month'] =  10
melt['Year'] =  2019
melt['Date'] = pd.to_datetime(melt[['Year', 'Month', 'Day']])

#Make Departure, Arrival, and Release time columns
melt['Dept Time'] = pd.to_datetime(melt['Year'].astype(str) + '/' + melt['Month'].astype(str) + '/' + melt['Day'].astype(str) + ' ' +melt['Dptr'].astype(str),utc=True)
melt['Arr Time'] = pd.to_datetime(melt['Year'].astype(str) + '/' + melt['Month'].astype(str) + '/' + melt['Day'].astype(str) + ' ' +melt['Arvl'].astype(str),utc=True)
melt['Rls Time'] = melt['Dept Time'] + pd.Timedelta(minutes=-90)

melt = melt.drop(columns=['BLK MINS', 'Dptr','Arvl','Year', 'Month', 'Day','Schd'])

#Make Hour Columns for each time
melt['Rls HR'] = melt['Rls Time'].dt.hour
melt['Dept HR'] = melt['Dept Time'].dt.hour
melt['Arr HR'] = melt['Arr Time'].dt.hour

melt['FltID'] = melt['Dept Time'].astype(str) + melt['Flt'].astype(str) + melt['Org'].astype(str) + melt['Dst'].astype(str)

#Print Sample
# print(melt)
# melt.dtypes

#Export melted df to a csv
# export_csv = melt.to_csv(r'oct_2019 MELT.csv', header=True) #CHANGE FILE NAME
# export_csv = melt['FltID'].to_csv(r'FltID.csv', header=True) #CHANGE FILE NAME

#Set day
daymelt = melt[melt['Day'] == 1]

#Get counts for each hour
Rhour = daymelt.groupby(['Rls HR']).count()[['Flt']]
Dhour = daymelt.groupby(['Dept HR']).count()[['Flt']]
Ahour = daymelt.groupby(['Arr HR']).count()[['Flt']]

#Merge counts into one table
HR1 = pd.merge(Rhour,Dhour,right_index=True, left_index=True,how='outer')
Hours = pd.merge(HR1,Ahour,right_index=True, left_index=True,how='outer')

#Plot
# Rplot = Rhour.plot.bar()
# Dplot = Dhour.plot.bar()
# Aplot = Ahour.plot.bar()
# Hours.plot.bar()

daymelt = melt[melt['Day'] == 1]
deskmelt = daymelt[daymelt['Desk'] == 1]

org_cities = deskmelt.filter(['Org','Desk','Rls HR'])
org_cities = org_cities.filter(['Org','Desk','Rls HR']).rename(columns={"Org": "City"})

dst_cities = deskmelt.filter(['Dst','Desk','Rls HR'])
dst_cities = dst_cities.filter(['Dst','Desk','Rls HR']).rename(columns={"Dst": "City"})

cities = org_cities.append(dst_cities).groupby(['Desk','Rls HR']).nunique()
cities = cities.filter(['City'])

num_cities = cities['City']
hrs = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]


# def cities_dist(hrs, num_cities):
#     plt.plot(hrs, num_cities)
# cities.plot.bar(y='City')

# cities_dist(hrs, num_cities)
