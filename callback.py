from tkinter import filedialog
import pandas as pd 

def upload_file():
    '''This Method allow user to import the .txt and csv file by clicking the Upload file button '''

    f_types = [('Text Document', '*.txt'),
               ('CSV files', "*.csv")]
    file = filedialog.askopenfilename(
        filetypes=f_types)

    if file:  # user selected one file
        global df 
        df = pd.read_csv(file)
        # print(fob.read())
    else:  # user cancel the file browser window
        print("No file chosen")



def main_column():
    '''The input is a list conatin orignal data frame coloumn in order to
    [timestamp, Azimuth, Elevation, range, rangerate, rcs ]

    example: orignal data frame coloum name -> [datae, timestamps in, timestamps out, azimuth, rcs, elevation, rangerate, range,]
    input would be [1,3,5,7,6,4] 
    This help to rearrange the coloumn and remove the extra coloumn
    '''
