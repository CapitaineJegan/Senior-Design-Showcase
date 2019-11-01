from tkinter import *
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import pandas as pd
#import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#importing filters
import csv
import numpy
df= pd.read_csv('oct_2019 MELT.csv')



#desk filter
def desk_filter(day,desk):
    global df2
    desk_new=[]
    for i in desk:
        desk_new.append(str(i))
    df1= df[df.Day.isin(day)]
    df2=df1[df1.Desk.isin(desk_new)]  #needs to be a string
    return (df2)

desk_filter([1],[3])
#print(df2)




class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        # create a horizontal scrollbar and the canvas
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        hscrollbar.pack(fill=X, side=BOTTOM, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE, anchor=W)
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

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


if __name__ == "__main__":

    class SampleApp(Tk):


        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)


            self.frame = VerticalScrolledFrame(root)
            self.frame.grid(row=0, column=0)
            #self.label = Label(text="Shrink the window to activate the scrollbar.")
            #self.label.grid(row=1, column=0)
            def graphdesk(desk):
            #print('you are printing imaginary graphs!')

                #placeholder dataframes

                Data1 = {'Country': ['US','CA','GER','UK','FR'],
                        'GDP_Per_Capita': [45000,42000,52000,49000,47000]
                       }

                df1 = DataFrame(Data1, columns= ['Country', 'GDP_Per_Capita'])
                df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()



                Data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
                        'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
                       }

                df2 = DataFrame(Data2,columns=['Year','Unemployment_Rate'])
                df2 = df2[['Year', 'Unemployment_Rate']].groupby('Year').sum()



                Data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
                        'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
                       }

                df3 = DataFrame(Data3,columns=['Interest_Rate','Stock_Index_Price'])

                #placeholder dataframes

                newWindow = tk.Toplevel()

                print(desk)
                figure1 = plt.Figure(figsize=(6,5), dpi=100)
                ax1 = figure1.add_subplot(111)
                bar1 = FigureCanvasTkAgg(figure1, newWindow)
                bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                df1.plot(kind='bar', legend=True, ax=ax1)
                ax1.set_title('Country Vs. GDP Per Capita')


                figure2 = plt.Figure(figsize=(5,4), dpi=100)
                ax2 = figure2.add_subplot(111)
                line2 = FigureCanvasTkAgg(figure2, newWindow)
                line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
                ax2.set_title('Year Vs. Unemployment Rate')


                figure3 = plt.Figure(figsize=(5,4), dpi=100)
                ax3 = figure3.add_subplot(111)
                ax3.scatter(df3['Interest_Rate'],df3['Stock_Index_Price'], color = 'g')
                scatter3 = FigureCanvasTkAgg(figure3, newWindow)
                scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
                ax3.legend()
                ax3.set_xlabel('Interest Rate')
                ax3.set_title('Interest Rate Vs. Stock Index Price')

            deskNum=tk.StringVar()
            entry_deskNum = tk.Entry(self.frame.interior, textvariable=deskNum, width=6).grid(row=0, column=0)
            button_graphdesk = tk.Button(self.frame.interior, text = 'Graph the desk!', command=lambda:graphdesk(deskNum.get())).grid(row=0, column=1, sticky='w'+'e')
            headers = []
            for col in df2.columns:
                #print(col)
                headers.append(col)
            headers[0] = 'Desk#'
            headerindex = 0
            for i in headers:
                tk.Label(self.frame.interior,text=i,font=("Helvetica", 8),bg = 'cyan',anchor= 'e',relief = 'solid').grid(row = 1, column = headerindex, sticky = 'w'+'e')
                headerindex +=1
            df2.to_csv('headless.csv', header=False, index=False)
            listedDF = df2.values.tolist()
            i_index = 2
            j_index = 0
            for i in listedDF:
                for j in i:
                    if i[0] < 101:
                        tk.Label(self.frame.interior, text=j,font=("Helvetica", 8),bg = 'lightgreen',anchor= 'e',relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                    else:
                        tk.Label(self.frame.interior,text=j,font=("Helvetica", 8),bg = 'orange', anchor = 'e', relief = 'solid').grid(row = i_index, column = j_index, sticky = 'w'+'e')
                    j_index +=1
                i_index +=1
                j_index = 0


    app = SampleApp()
    app.mainloop()
