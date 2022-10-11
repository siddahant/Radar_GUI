import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from collections import Counter
from sklearn.cluster import DBSCAN

def ploar2xyz(df):
    '''Convert polar cordinate to xyz cordinate
    '''
    x = df['range'] * np.cos(df['Elevation']) * np.cos(df['Azimuth'])
    y= df['range'] * np.cos(df['Elevation']) * np.sin(df['Azimuth'])
    z = df['range'] * np.sin(df['Elevation'])
    df.insert(6, "x", x, True) 
    df.insert(7, "y", y, True) 
    df.insert(8, "z", z, True) 
    return df

def isdeg(angle):
  if max(angle)> 1.57079028204:
    return angle*np.pi/180
  return angle

def filter(df,filter_Name,min_val="", max_val=""):
  filters={"A": "Azimuth",
           "E": "Elevation",
           "V": "rangerate",
           "R":"range",
           "P":'power',
           "X":"x",
           "Y":"y",
           "Z":"z",
           "T":"timestamps"}
  
  if min_val == "":
    min_val = min(df[filters[filter_Name]])
  if max_val == "": 
    max_val = max(df[filters[filter_Name]])

  if (filter_Name=="A" or filter_Name=="E") and min_val != "":
    min_val = float(min_val)*np.pi/180

  if (filter_Name=="A" or filter_Name=="E") and max_val != "":
    max_val = float(max_val)*np.pi/180


  return df[(df[filters[filter_Name]] >= float(min_val)) & (df[filters[filter_Name]] <= float(max_val))]

