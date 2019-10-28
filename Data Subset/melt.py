import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

df = pd.read_excel('fullHistWeights.xlsx', sheet_name='fullHistWeights') #CHANGE FILE AND SHEET NAMES
df2 = pd.read_excel('regionMapping.xlsx', sheet_name='regionMapping') #CHANGE FILE AND SHEET NAMES
df3 = pd.read_excel('regionMapping2.xlsx', sheet_name='regionMapping') #CHANGE FILE AND SHEET NAMES

#THIS MELTS DF
melt = pd.melt(df, id_vars=['Year','Month','Flt','Org','Dst','Eqt','Dptr','Arvl','BLK MINS','MILES','Desk','Flight ID','Value Sum','Mile Val','Airport','Spec1 - NYC ATC','Reserved'] 
	,value_vars=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
	,var_name = 'Day'
	,value_name = 'Schd')



melt = melt.dropna(subset=['Schd'])
# melt['City Pair'] =  melt['Org'] + '-' + melt['Dst']

#JOIN DF2 FOR ORIG REGION
melt = melt.join(df2.set_index('Station'), on='Org')

#JOIN DF3 FOR DEST REGION
melt = melt.join(df3.set_index('Station'), on='Dst')

#DROPS ALL FLIGHTS THAT DO NOT HAVE A REGION. REMOVES ALL INTERNATIONAL/RANDOM STATIONS
melt = melt.dropna(subset=['Orig Region','Dest Region'])
# print(melt)
export_csv = melt.to_csv(r'FULLmelt.csv', header=True) #CHANGE FILE NAME


#Don't forget to add '.csv' at the end of the path