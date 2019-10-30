import pandas as pd 
import csv 
import numpy as np
df= pd.read_csv('oct_2019 MELT.csv')


#FLIGHT FILTER
#Def: filters flights by origin, destination, day, and hour
    #inputs:
        #df: melted data frame
        #origin: list of strings
        #destination: list of strings
        #day: list of integers
        #hour: list of integers
    #Description: it checks whether there is an empty input(s) 
    #Return:new dataframe with filtered flights by origin,destination,day, and hour

def flight_filter(df, org,dest,day_,hour_):
    day=[]
    hour=[]
    for d in day_:
        day.append(np.int64(d))
    for h in hour_:
        hour.append(np.int64(h))
  
            
#     return(len(org),len(dest),len(day),len(hour))
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)>0:  #no org
        
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
#         return(type(df['Org'][0]),type(df['Dst'][0]),type(df['Day'][1])==numpy.int64,type(df['RlsHR'][1])==numpy.int64)
        return fl3


    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no dest
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3

    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return fl3
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        return fl3
        
    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no org,dest
        fl1=df[df.Day.isin(day)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no org,day
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no org,hour
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2
        
    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #no dest,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        return fl2
    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #no dest,day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return fl2
    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #no day,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        return fl2
    
    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #only org
        fl1=df[df.Org.isin(org)]
        return fl1
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #only dest
        fl1=df[df.Dst.isin(dest)]
        return fl1
    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #only day
        fl1=df[df.Day.isin(day)]
        return fl1
    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #only hour
        fl1=df[df.Rls_HR.isin(hour)]
        return fl1
        
    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #none entered
        return df
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)>0:
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        fl4=fl3[fl3.Rls_HR.isin(hour)]
        return fl4

org=['ATL']
dest=[]
day_=[2,3]
hour_=[2]     
print(flight_filter(df, org,dest,day_,hour_))
