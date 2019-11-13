import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import ntpath #for taking file name only - still working on that.
from tabulate import tabulate
from tkinter import *
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#importing filters
import csv
import numpy
import random
import numpy as np
colList = ['Flt', 'Org', 'Dst', 'Eqt', 'MILES', 'Date', 'Dept_Time', 'Arr_Time', 'Rls_Time', 'Desk']
testDF = filtered_flights.filter(items = colList)
#print(testDF)
listedFlt = testDF.reset_index().values.tolist()
type(listedFlt[0][1])
for i in listedFlt:
    i[1]=int(i[1])
    i[5]=int(i[5])
    i[9]=i[9][11:16]
    i[7]=i[7][11:16]
    i[8]=i[8][11:16]
#testTime = listedFlt[0][6]
