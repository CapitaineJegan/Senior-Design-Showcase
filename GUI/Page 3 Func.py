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

#### Page 3 functions ####
###TK for Page 3 scrollbar class###
    
# [PAGE 3] desk filter
def desk_filter(day,desk):
    global df2
    desk_new=[]
    for i in desk:
        desk_new.append(str(i))
    df1= df[df.Day.isin(day)]
    df2=df1[df1.Desk.isin(desk_new)]  #needs to be a string
    return (df2)

desk_filter([1],[3]) #Calls desk filter function from the Filters section. Fixed results.
#print(df2)

### Melt function from Integration_cities ###
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

### [PAGE 3] graphs desks for three fixed graphs taken from the data of sep_2019.xlsx
def graphdesk(desk):
    #placeholder dataframes

    newWindow = tk.Toplevel()   #New popup window for Visualizer
    newWindow.title("Visualizer")
    
    newWindow.geometry('%dx%d+%d+%d' % (1800, 800, 100, 100))   #Layers the Visualizer window over the others
    
    ###Jake's 'Graph from Data' code###
    file = 'sep_2019.xlsx' #fixes file name
    melt = melt_file(file) #calls melt function above
    date = '09-01-2019'  #fixes date
    desks = ['M87', 1]  #fixes the desk list for all possible desks
    desk_filter_data = desk_filter(melt, date, desks) #calls the desk_filter function and stores the 
    desk_display_df = desk_display(melt, date, desks) #calls the desk_display function and stores the returned dataframes
    
    desk = 'M87' #Fixes desk chosen as M87
    
    #For showing the three graphs onto the popup
    workload_dist(desk, newWindow)
    releases_dist(desk, newWindow)
    cities_dist(desk_filter_data, newWindow)

#Jake's scrollbar class, takes in Frame, where the scrollbar is used. Vertical scrolling only
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
#            hscrollbar = Scrollbar(self, orient=HORIZONTAL)
#            hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
            canvas = Canvas(self, bd=0, highlightthickness=0, width=2500, height=800, yscrollcommand=vscrollbar.set)#, xscrollcommand=hscrollbar.set)
            canvas.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=W)
            vscrollbar.config(command=canvas.yview)
#            hscrollbar.config(command=canvas.xview)

            # reset the view
#            canvas.xview_moveto(0)
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

### [PAGE 3 DESK] Shows a new window for the Desks connected to Page 2's left side, and Maximum Releases, Flights, and Stations per hour in a table ###
def makeP3a():
    page3a = tk.Toplevel()  #Page 3a window used for this page
    page3a.geometry('%dx%d+%d+%d' % (500, 880, 400, 80))
    
    p3frame = VerticalScrolledFrame(page3a) #Calls the scrollbar class to fit a scrollbar onto the frame in the middle of the window
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)
    
    deskNum=tk.StringVar() #variable to store the desk number to be used in the visualization entry box. 
    
    #visualization for graphs, calls the graphdesk function
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0, sticky='e') #Entry box to search for the appropriate desk. Single desk entry only (no lists)
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w')
    
    headers = [] #list of names for the headers in Page 3, for the columns
    
    headers = ['Desk#', 'Max. # of Releases/hr', 'Max # of Flights/hr', 'Max # of Stations/hr'] #The header names in a list
    headerindex = 0 #Index for use in showing headers on the frame with a for function
    
    #Hardcoding random variables; will replace with max_XXX functions in next version
    for x in range(100):
        a=random.randint(1,20)  #random nummbers for workload/releases
        b=random.randint(1,20)  #random nummbers for flights
        c=random.randint(1,10)  #random nummbers for stations/cities
        
        if a > 10 or b > 10 or c > 5: #Sets the threshold for green and red rows, according to the value of each variable
            tk.Label(p3frame.interior, text=random.randint(1,100), font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=0, sticky='w'+'e')
            tk.Label(p3frame.interior, text=a, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=1, sticky='w'+'e')
            tk.Label(p3frame.interior, text=b, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=2, sticky='w'+'e')
            tk.Label(p3frame.interior, text=c, font=("Helvetica", 8),bg = 'pink', anchor = 'e', relief = 'solid').grid(row=x+1, column=3, sticky='w'+'e')
        else:
            tk.Label(p3frame.interior, text=random.randint(1,100), font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=0, sticky='w'+'e')
            tk.Label(p3frame.interior, text=a, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=1, sticky='w'+'e')
            tk.Label(p3frame.interior, text=b, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=2, sticky='w'+'e')
            tk.Label(p3frame.interior, text=c, font=("Helvetica", 8),bg = 'lightgreen', anchor = 'e', relief = 'solid').grid(row=x+1, column=3, sticky='w'+'e')
    
    ##########
    
    for i in headers:   #Sets header color as cyan and places them at the top of the frame
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 12), bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1
    
    #puts refresh and back buttons; refresh calls p3arefresh, to close and reopen this window. Back calls p3aclose and closes the current window and go back to page 2
    tk.Button(page3a,text="Refresh", font=('helvetica', 12), command=lambda: p3arefresh(page3a)).grid(row=0,column=1, sticky="E")
    tk.Button(page3a, text="Back", font=('helvetica', 12), command=lambda: p3aclose(page3a)).grid(row=3, column=0, sticky="W")

# [PAGE 3 FLIGHT] Window for Flights page connected to Page 2's right side
def makeP3b():
    page3b = tk.Toplevel()  #the window variable name used for this function
    page3b.geometry('%dx%d+%d+%d' % (1180, 890, 400, 80))   #fixes location and size for the window
    
    p3frame = VerticalScrolledFrame(page3b) #Calls the scrollbar class to fit a scrollbar onto the frame in the middle of the window
    p3frame.grid(row=1, column=0, columnspan=2, rowspan=2)
    #self.label = Label(text="Shrink the window to activate the scrollbar.")
    #self.label.grid(row=1, column=0)
    
#    def graphdesk(desk):
#    #print('you are printing imaginary graphs!')
#
#        newWindow = tk.Toplevel()
#        newWindow.title("Visualizer")
#        
#        newWindow.geometry('%dx%d+%d+%d' % (1800, 800, 100, 100))
#        
#        ###Jake's 'Graph from Data' code###
#        file = 'sep_2019.xlsx'
#
#
#        melt = melt_file(file)
#        date = '10-01-2019'
#        desks = ['M87', 1]
#        desk_filter_data = desk_filter(melt, date, desks)
#        desk_display_df = desk_display(melt, date, desks)
#        
#        desk = 'M87'
#        workload_dist(desk, newWindow)
#        releases_dist(desk, newWindow)
#        cities_dist(desk_filter_data, newWindow)
        #########
    
    deskNum=tk.StringVar() #variable to store the desk number to be used in the visualization entry box. Single desk entry only (no lists)
    headers = [] #list of names for the headers in Page 3, for the columns
    headers[0] = 'Desk#' #The header names in a list
    headerindex = 0 #Index for use in showing headers on the frame with a for function
    
    #visualization for graphs, calls the graphdesk function
    tk.Entry(p3frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0) #Entry box to search for the appropriate desk. Single desk entry only (no lists)
    tk.Button(p3frame.interior, text = 'Visualize', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w'+'e')
    
    for col in df2.columns: #Takes in the column names directly from the dataframe
        #print(col)
        headers.append(col)
    
    for i in headers: #puts the headers onto the top of the frame, in cyan color
        tk.Label(p3frame.interior,text=i,font=("Helvetica", 8),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
        headerindex +=1
    
    df2.to_csv('headless.csv', header=False, index=False) #fixed to call the headless.csv file by default
    listedDF = df2.values.tolist() #stores the dataframe values from desk_filter
    i_index = 2 #starting indices for the data to be shown, set so that it ignores the headers and goes straight to the data
    j_index = 0
    
    for i in listedDF: #iterates over the whole dataframe, shows the data in light green if the desk index is 100 or less, and orange otherwise
        for j in i:
            if i[0] < 101:
                tk.Label(p3frame.interior, text=j,font=("Helvetica", 8),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            else:
                tk.Label(p3frame.interior,text=j,font=("Helvetica", 8),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
            j_index +=1
        
        i_index +=1
        j_index = 0
    
    #refresh and back buttons. Refresh calls p3brefresh, closing and reopening this window; Back calls p3bclose, closing this window and opening Page 3 again.
    tk.Button(page3b,text="Refresh", font=('helvetica', 12), command=lambda: p3brefresh(page3b)).grid(row=0,column=1, sticky="E")
    tk.Button(page3b, text="Back", font=('helvetica', 12), command=lambda: p3bclose(page3b)).grid(row=3, column=0, sticky="W")