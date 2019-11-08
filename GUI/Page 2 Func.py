#### [PAGE 2 LEFT] Next button functions. Variables are desk, day1 corresponding to p1 and p2, input as lists
#### p2aCategories, deskList, and dayList are global
def savep2dskInfo(page, p1, p2):
    p2aCategories = []  #refreshes the lsit so it's cleared each time the button is pressed
    p2aCategories.append(p1)    #Adds the Desks and Days that are given by the entry boxes in Page 2
    p2aCategories.append(p2)    #These are for storing the general lists, not for manipulation
    print(p2aCategories)
    
    deskList = []
    day1List = []
    
    deskList = list(p1.split(",")) #splits the input from Page 2 by commas for easier 
    day1List = list(p2.split(","))
    
    try:    #Will turn the entry into a proper set of strings into a list
        day1List = list(map(int, day1List))
        
    except: #Planning on turning this into the defaulting function where all datapoints are selected if the entries are left blank
        print()
    
    print(deskList, day1List)
    page.destroy() #Closes Page 2
    makeP3a() #Opens Page 3, see makeP3a below

#### [PAGE 2 FLIGHT] saves the information on page 2 for Flight side, then closes the window and moves onto page 3b, similar to above function for Desk and page 3a
#### Mostly the same comments as savep2dskInfo above, but with origin, destination, day2, and hour variables instead
def savep2fltInfo(page, p3, p4, p5, p6):
    p2bCategories = []
    p2bCategories.append(p3)
    p2bCategories.append(p4)
    p2bCategories.append(p5)
    p2bCategories.append(p6)
    print(p2bCategories)
    
    origList = []
    destList = []
    day2List = []
    hourList = []
    
    origList = list(p3.split(","))
    destList = list(p4.split(","))
    day2List = list(p5.split(","))
    hourList = list(p6.split(","))
    
    try:
        day2List = list(map(int, day2List))
        
    except:
        print()
    
    print(origList, destList, day2List, hourList)
    
    page.destroy()
    makeP3b()

#### [PAGE 2] Window, entries, labels, and buttons
def makeP2():
    ###Page 2a and 2b code###
    page2b=tk.Toplevel()    #Window for Page 2, called "Desks & Flights"
    page2b.title("Desks & Flights")
    
    page2b.geometry('%dx%d+%d+%d' % (780, 200, 500, 200))   #layers Page 2 over Page 1, sets size
    
    #variables for the entries in 2b, basically what you'd type in to search in the desk and flight fields
    p2desk = tk.StringVar(page2b)
    p2day1 = tk.StringVar(page2b)
    p2orig = tk.StringVar(page2b)
    p2dest = tk.StringVar(page2b)
    p2day2 = tk.StringVar(page2b)
    p2hour = tk.StringVar(page2b)
    
    #stores a value for if the All boxes are ticked. 1 is True, 0 is False. Will rework into selecting all the information by default
#    origAll = tk.IntVar()
#    destAll = tk.IntVar()
#    day2All = tk.IntVar()
#    hourAll = tk.IntVar()
    
    ###Page 2a (LEFT side) code###
    tk.Label(page2b, text = 'Desks',font=('helvetica', 16)).grid(row=0, column=0, columnspan = 3, sticky="W"+"E") #Header for Desks
    
    #label for Desk on left side, saves the entry variable into p2desk
    tk.Label(page2b, text = 'Desk',font=('helvetica', 14)).grid(row=1, column=0, sticky="W") 
    entryDesk = tk.Entry(page2b, textvariable = p2desk, width=50)
    entryDesk.grid(row=1, column=1, columnspan=2)
    
    #label for Day on left side, saves the entry variable into p2day1
    tk.Label(page2b, text = 'Day',font=('helvetica', 14)).grid(row=2, column=0, sticky="W") 
    entry_day = tk.Entry(page2b, textvariable = p2day1, width=50)
    entry_day.grid(row=2, column=1, columnspan=2)
    
    #Next button, for the left side, goes to Page 3a after going through savep2dskInfo
    p2Nextdsk = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2dskInfo(page2b, p2desk.get(), p2day1.get()))
    p2Nextdsk.grid(row=3, column=1, sticky="W"+"E") 
    
    ###Page 2b (RIGHT side) code end###
    #Flights label, pair on the right side of Desks with column span of 3 instead of 2
    #to accommodate the "All" checkboxes
    tk.Label(page2b, text="Flights",font=('helvetica', 16)).grid(row=0, column=3, columnspan=4, sticky="W"+"E") #Header for Flights
    
    #Origin, saves entry variable in p2orig
    tk.Label(page2b, text="Origin",font=('helvetica', 14)).grid(row=1, column=3, sticky="W")
    entryOrig = tk.Entry(page2b, textvariable = p2orig, width=50)
    entryOrig.grid(row=1, column=4, columnspan=2)
    
    #Destination, saves entry variable in p2dest
    tk.Label(page2b, text="Destination",font=('helvetica', 14)).grid(row=2, column=3, sticky="W")
    entryDest = tk.Entry(page2b, textvariable = p2dest, width=50)
    entryDest.grid(row=2, column=4, columnspan=2)
    
    #Day, int, saves entry variable in p2day2
    tk.Label(page2b, text="Day",font=('helvetica', 14)).grid(row=3, column=3, sticky="W")
    entryDay2 = tk.Entry(page2b, textvariable = p2day2, width=50)
    entryDay2.grid(row=3, column=4, columnspan=2)
    
    #Hour, string, saves entry variable in p2hour
    tk.Label(page2b, text="Hour",font=('helvetica', 14)).grid(row=4, column=3, sticky="W")
    entryHour = tk.Entry(page2b, textvariable = p2hour, width=50)
    entryHour.grid(row=4, column=4, columnspan=2)
    
    #Back button, closes Page 2 if clicked
    tk.Button(page2b, text="Back",font=('helvetica', 12), command=lambda: page2b.destroy()).grid(row=5, column=0, sticky="W"+"E") 
    
    #Next button for Flights, calls savep2fltInfo above
    p2Nextflt = tk.Button(page2b, text="Next",font=('helvetica', 12), command=lambda: savep2fltInfo(page2b, p2orig.get(), p2dest.get(), p2day2.get(), p2hour.get()))
    p2Nextflt.grid(row=5, column=4, sticky="W"+"E") #Next button for flights (right side)
#### Page 2b code end ####
    
    