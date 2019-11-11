def NEW_event_hours(df,handoff_df):
    '''
    Def: Generates dataframe of flight events each hour for one desk
    Inputs:
        df: desk_filter dataframe
    Return: new dataframe fl_id indexes, columns for each hour,
        and what event happens in each hour (rls, dep, mon, arr)
    '''
    events = pd.DataFrame(columns = [i for i in range(0, 24)] + ['Desk'])
    for i in range(len(df)):
        desk = [df.iloc[i]['Desk']]
        if len(desk[0]) == 1:
            desk[0] = 'A0' + desk[0]
        if desk[0][0] == 'P' and len(desk[0]) == 2:
            desk[0] = desk[0][0] + '0' + desk[0][1]
        print(desk[0])
        handoff_df['Desk_Ind'] = handoff_df['DESK'].str.find(desk[0])
        desk_subset = handoff_df[handoff_df['Desk_Ind'] == 0].values
        
        start_shift_desk = desk_subset[0][1]
        end_shift_desk = desk_subset[0][2]
        recieve = desk_subset[0][3]
        transfer = desk_subset[0][4]
        
        print('Recieved from:', recieve)
        print('Transfer to:', transfer)
        
        if recieve == '***':
            rec_subset = []
        else:
            handoff_df['Rec_Ind'] = handoff_df['DESK'].str.find(recieve)
            rec_subset = handoff_df[handoff_df['Rec_Ind'] == 0].values  
        
        end_shift_rec = rec_subset[0][2]
        
        print(rec_subset)