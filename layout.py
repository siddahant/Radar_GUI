from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from callback import *
###############################################################################
#                            Layout                                           # 
###############################################################################

root = Tk()
root.geometry("1366x786")  # Size of the window
root.title('RADAR')
my_font = ('times', 14)

###############################################################################
#                            Buttons                                          # 
###############################################################################

# uploading file 
'''File upload button helps to import cvs file and text document'''
file_upload_button = Button(root, text='Upload File',
                            width=20, command=lambda: upload_file(), fg="blue")
# selecting main coloums
'''This buttom allow to filter the main columns and arrange the data frame'''
main_column_button = Button(root, text='Main columns',
                            width=20, command=lambda: main_column(), fg="blue")


###############################################################################
#                            Locations                                        # 
###############################################################################

file_upload_button.grid(row=0, column=0, columnspan=1)
main_column_button.grid(row=1, column=0, columnspan=1)
