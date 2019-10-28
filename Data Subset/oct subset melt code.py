import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('oct_2019.xlsx', sheet_name='All Flights') #CHANGE FILE AND SHEET NAMES
df2 = pd.read_excel('regionMapping.xlsx', sheet_name='regionMapping') #CHANGE FILE AND SHEET NAMES
df3 = pd.read_excel('regionMapping2.xlsx', sheet_name='regionMapping') #CHANGE FILE AND SHEET NAMES

df = df.join(df2.set_index('Station'), on='Org')
df = df.join(df3.set_index('Station'), on='Dst')
df = df.dropna(subset=['Orig Region','Dest Region'])

#THIS MELTS DF
melt = pd.melt(df, id_vars=['Flt','Org','Dst','Eqt','Dptr','Arvl','BLK MINS','MILES','Desk']
	,value_vars=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
	,var_name = 'Day'
	,value_name = 'Schd')

# print(melt['Dptr'])

melt = melt.dropna(subset=['Schd'])
melt['Month'] =  10
melt['Year'] =  2019
melt['Date'] = pd.to_datetime(melt[['Year', 'Month', 'Day']])

melt['Dept Time'] = pd.to_datetime(melt['Year'].astype(str) + '/' + melt['Month'].astype(str) + '/' + melt['Day'].astype(str) + ' ' +melt['Dptr'].astype(str))
# melt['Dept Time'] = pd.to_datetime(melt['Dept Time'])
melt['Arr Time'] = pd.to_datetime(melt['Year'].astype(str) + '/' + melt['Month'].astype(str) + '/' + melt['Day'].astype(str) + ' ' +melt['Arvl'].astype(str))

# melt['Arr Time'] = pd.to_datetime(melt['Date'],melt['Arvl'])
melt['Rls Time'] = melt['Dept Time'] + pd.Timedelta(minutes=-90)

# hours = melt['Rls Time'].dt.hour

# melt['Rls HR'] = pd.melt['Rls Time'].dt.hour
# melt['Dept HR'] = melt['Dept Time'].dt.hour
# melt['Arr HR'] = melt['Arr Time'].dt.hour
# print(melt['Arr Time'])
# melt = melt.join(df2.set_index('Station'), on='Org')

# melt = melt.join(df3.set_index('Station'), on='Dst')

# melt = melt.dropna(subset=['Orig Region','Dest Region'])
print(melt.head())
# export_csv = melt.to_csv(r'oct_2019.csv', header=True) #CHANGE FILE NAME


#Don't forget to add '.csv' at the end of the path
