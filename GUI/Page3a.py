from tkinter import *   # from x import * is bad practice
import pandas as pd
import tkinter as tk
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
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
                print('you are printing imaginary graphs!')
                print(desk)

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
