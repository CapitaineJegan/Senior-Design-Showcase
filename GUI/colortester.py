import tkinter as tk
from tkinter import filedialog
import pandas as pd
#import numpy as np
from tabulate import tabulate

#importing filters
import csv
import numpy
df= pd.read_csv('oct_2019 MELT.csv')


#desk filter
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

desk_filter(df, [1],[3])
#print(df2)
index = 0

coloringtester = tk.Tk()
#for index, row in df2.iterrows():
    #print(index)
    #print(row)
    #tk.Label(coloringtester, text=row,font=("Helvetica", 16)).grid(row=0, column=0)
#for i in range(len(df2)):
   # print(df2.iloc[i])
    #emplist = []
    #emplist.append()
    #tk.Label(coloringtester, text=df2.iloc[i],font=("Helvetica", 16)).pack()
layout = tabulate(df2)
#print(layout)
#alist = [[1,2,3],[4],[5,6]]
#for i in alist:
#    print(i)
#    tk.Label(coloringtester, text=i,font=("Helvetica", 16)).pack()
#coloringtester.mainloop()
#print(df2.to_csv(header=None, index=False))
headers = []
for col in df2.columns:
    #print(col)
    headers.append(col)
headers[0] = 'Desk#'
headerindex = 0
for i in headers:
    tk.Label(coloringtester, text=i,font=("Helvetica", 16),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 0, column = headerindex, sticky = 'w'+'e')
    headerindex +=1
df2.to_csv('headless.csv', header=False, index=False)
headless = df2.to_csv(header = None, index=False)
listedDF = df2.values.tolist()
i_index = 1
j_index = 0
for i in listedDF:
    for j in i:
        if i[0] < 101:
            tk.Label(coloringtester, text=j,font=("Helvetica", 16),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
        else:
            tk.Label(coloringtester, text=j,font=("Helvetica", 16),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
        j_index +=1
    i_index +=1
    j_index = 0
coloringtester.mainloop()
