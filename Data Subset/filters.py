import pandas as pd 
import csv 
import numpy
df= pd.read_csv('oct_2019 MELT.csv')


#desk filter
def desk_filter(day,desk):
    desk_new=[]
    for i in desk:
        desk_new.append(str(i))
        
    df1= df[df.Day.isin(day)]
    df2=df1[df1.Desk.isin(desk_new)]  #needs to be a string
    return (df2)
    
desk_filter([1],[3])

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

def flight_filter(org,dest,day_,hour_):
    day=[]
    hour=[]
    for d in day_:
        day_num.append(numpy.int64(d))
    for h in hour_:
        hour_num.append(numpy.int64(h))
  
            
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
        return f13
    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Rls_HR.isin(hour)]
        return f13
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no hour
        fl1=df[df.Org.isin(org)]
        fl2=flf1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        return f13
        
    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)>0:  #no org,dest
        fl1=df[df.Day.isin(day)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return f12
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)>0:  #no org,day
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return f12
    if len(org)==0 and len(dest)>0 and len(day)>0 and len(hour)==0:  #no org,hour
        fl1=df[df.Dst.isin(dest)]
        fl2=fl1[fl1.Day.isin(day)]
        return f12
        
    if len(org)>0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #no dest,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Day.isin(day)]
        return f12
    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #no dest,day
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Rls_HR.isin(hour)]
        return f12
    if len(org)>0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #no day,hour
        fl1=df[df.Org.isin(org)]
        fl2=fl1[fl1.Dst.isin(dest)]
        return f12
    
    if len(org)>0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #only org
        fl1=df[df.Org.isin(org)]
        return f11
    if len(org)==0 and len(dest)>0 and len(day)==0 and len(hour)==0:  #only dest
        fl1=df[df.Dst.isin(dest)]
        return f11
    if len(org)==0 and len(dest)==0 and len(day)>0 and len(hour)==0:  #only day
        fl1=df[df.Day.isin(day)]
        return f11
    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)>0:  #only hour
        fl1=df[df.Rls_HR.isin(hour)]
        return f11
        
    if len(org)==0 and len(dest)==0 and len(day)==0 and len(hour)==0:  #none entered
        return df
    if len(org)>0 and len(dest)>0 and len(day)>0 and len(hour)>0:
        fl1=df[df.Org.isin(org)]
        fl2=flf1[fl1.Dst.isin(dest)]
        fl3=fl2[fl2.Day.isin(day)]
        fl4=fl3[fl3.Rls_HR.isin(hour)]
        return fl4
        
flight_filter([],['ATL'],[2],[19])



