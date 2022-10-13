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




def sep_algo(filter_data,eps_value,test):
    timestamp = filter_data.timestamps.unique()
    sepration_angle = []
    l_target_rcs = [] 
    r_target_rcs = []
    center_pos_rcs =[]
    r_point=[]
    l_point=[]
    c_point=[]
    n_clusters_list=[]
    n_noise_list=[]
    color_list=[]
    if test=="Azimuth":
      col_variable=['x','y']
    else :
      col_variable=['x','z']

    for i in timestamp:
        frame = filter_data[filter_data['timestamps']== i]
        dbscan_data=frame[col_variable].values.astype('float32',copy=False)
        model = DBSCAN(eps=eps_value, min_samples=2, metric='euclidean').fit(dbscan_data)
        labels=model.labels_
        color_list.extend(labels)

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_clusters_list.append(n_clusters_)
        n_noise_list.append( list(labels).count(-1))

        if n_clusters_ >= 2:
            target_1=frame[model.labels_ == 0]
            target_2=frame[model.labels_ == 1]

            if target_1[test].mean()<target_2[test].mean():
                l_target = target_1
                r_target = target_2
            else:
                l_target = target_2
                r_target = target_1

            c_point.append(0)
            sepration_angle.append((abs(target_1[test].mean()-target_2[test].mean()))*180/np.pi)
            
            l_target_rcs.append(l_target['power'].mean())
            r_target_rcs.append(r_target['power'].mean())
            l_point.append(len(l_target))
            r_point.append(len(r_target))
            
        else:
            target_c=frame[model.labels_ == 0]
            sepration_angle.append(0)
            center_pos_rcs.append(target_c['power'].mean())
            l_point.append(0)
            r_point.append(0)
            c_point.append(len(target_c))
    if len( center_pos_rcs)==0:
       center_pos_rcs =[0]
    if len( l_target_rcs )==0:
      l_target_rcs = [0] 
    if len( r_target_rcs )==0:
      r_target_rcs = [0] 
    return frame,labels,n_clusters_list,sepration_angle,timestamp,l_target_rcs,center_pos_rcs, r_target_rcs,l_point,r_point,c_point,color_list

