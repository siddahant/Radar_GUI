import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
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

def get_sepration_info(targets):
  sepration_list=[]
  for i in targets:
    if len(i)==3:
      sepration_list.append("p")
    elif len(i)==1:
      if "l" in i or "r" in i:
        sepration_list.append("b")
      else:
        sepration_list.append("m")
    elif ("l" in i) and ("r" in i):
      sepration_list.append("s")
  sepration_percentage=(sepration_list.count('s')/len(sepration_list))*100
  blink_percentage=(sepration_list.count('b')/len(sepration_list))*100
  mean_pose_percentage = (sepration_list.count('m')/len(sepration_list))*100
  partial_sepration_percentage = (sepration_list.count('p')/len(sepration_list))*100
  percentage = {"sepration" : sepration_percentage, 
                "blink" : blink_percentage,
                "mean_pose" :mean_pose_percentage,
                "partial_sepration":partial_sepration_percentage}
  return percentage


def run_dbscan(target_data,test):

    if test=="Elevation":
      col_variable=['x','z']
    else :
      col_variable=['x','y']

    dbscan_data=target_data[col_variable].values.astype('float32',copy=False)
    eps_value = 0.1
    increase_eps_value = True
    if dbscan_data.shape[0] > 1:
      while increase_eps_value:
        model = DBSCAN(eps=eps_value, min_samples=2, metric='euclidean').fit(dbscan_data)
        labels=model.labels_
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        if n_clusters_ == 1:
          increase_eps_value = False
        else:
          eps_value = eps_value + eps_value*.5

    elif dbscan_data.shape[0] == 1:
      labels = np.array([0])
    else:
      labels = np.array([])
    return labels  


def sep_algo(filter_data,test,thershold_wall_min, thershold_wall_max):
    temp_labels = []
    if test == "Azimuth":
      parameter ='y'
    else:
      parameter ='z'
    
    for xpos in filter_data[parameter]:
        if (thershold_wall_min > xpos) and (thershold_wall_max> xpos):
            temp_labels.append('l')
        elif (thershold_wall_min < xpos) and (thershold_wall_max < xpos):
            temp_labels.append('r')
        else:
            temp_labels.append('c')
    timestamp = filter_data.timestamps.unique()
    algo_data = filter_data.copy()
    algo_data.insert(9, "labels", temp_labels,allow_duplicates=False)
    left_target_rcs = []
    right_target_rcs = []
    mean_pose_rcs =[]
    right_point=[]
    left_point=[]
    mean_pose_point=[]
    sepration_angle=[]
    targets = []
    color_labels=[]
    for i in timestamp:
        target_detected = []
        frame = algo_data[algo_data['timestamps']== i]
        right_target_data = frame[frame['labels'] == 'r']
        right_target_labels = run_dbscan(right_target_data,test)
        frame.reset_index(inplace = True, drop = True)
        if len(right_target_labels) != 0:
            right_target_data = right_target_data[right_target_labels== 0]
            target_detected.append('r')
            right_target_rcs.append(right_target_data['power'].mean())
            right_point.append(len(right_target_data))
            color_list = (["r" if label==0 else "k" for label in right_target_labels])
            j=0
            for row in range(len(frame)):
              if frame.loc[row,'labels'] == 'r':
                frame.loc[row,'labels'] = color_list[j]
                j +=1
        else:
          right_point.append(0)

        left_target_data = frame[frame['labels'] == 'l']
        left_target_labels = run_dbscan(left_target_data,test)
        if len(left_target_labels) != 0:
            left_target_data = left_target_data[left_target_labels==0]
            target_detected.append('l') 
            left_target_rcs.append(left_target_data['power'].mean())
            left_point.append(len(left_target_data))
            color_list=(["b" if label==0 else "k" for label in left_target_labels])
            j=0
            for row in range(len(frame)):
              if frame.loc[row,'labels'] == 'l':
                frame.loc[row,'labels'] = color_list[j]
                j +=1
        else:
          left_point.append(0)
        
        if len(left_target_labels) != 0 and (len(right_target_labels) != 0):
            sepration_angle.append((abs(left_target_data['Azimuth'].mean()-right_target_data['Azimuth'].mean()))*180/np.pi)
        else:
            sepration_angle.append(0)

        mean_pose_data = frame[frame['labels'] == 'c']
        mean_pose_labels = run_dbscan(mean_pose_data,test)
        if len(mean_pose_labels) != 0:
            mean_pose_data =  mean_pose_data[mean_pose_labels==0]
            target_detected.append('c')
            mean_pose_rcs.append(mean_pose_data['power'].mean())
            mean_pose_point.append(len(mean_pose_data))
            color_list = (["g" if label==0 else "k" for label in mean_pose_labels])
            j=0
            for row in range(len(frame)):
              if frame.loc[row,'labels'] == 'c':
                print(frame)
                print(j)
                print(color_list)
                frame.loc[row,'labels'] = color_list[j]
                j +=1
        else:
          mean_pose_point.append(0)

        color_labels.extend (frame['labels'].tolist())    
        targets.append(target_detected)

    if len(mean_pose_rcs)==0:
      mean_pose_rcs =[0]
    if len( left_target_rcs )==0:
      left_target_rcs = [0] 
    if len( right_target_rcs )==0:
      right_target_rcs = [0] 

    percentage = get_sepration_info(targets)
    res = {"left_target_rcs" : left_target_rcs,
        "right_target_rcs": right_target_rcs,
        "mean_pose_rcs" : mean_pose_rcs,
        "right_point" : right_point,
        "left_point" : left_point,
        "mean_pose_point" :mean_pose_point,
         "percentage" : percentage,
         "timestamp" : timestamp,
         "sepration_angle":sepration_angle,
         "color_labels": color_labels}
    return res







































# def sep_algo_temp(filter_data,eps_value,test):
#     timestamp = filter_data.timestamps.unique()
#     sepration_angle = []
#     l_target_rcs = [] 
#     r_target_rcs = []
#     center_pos_rcs =[]
#     r_point=[]
#     l_point=[]
#     c_point=[]
#     n_clusters_list=[]
#     n_noise_list=[]
#     color_list=[]
#     if test=="Azimuth":
#       col_variable=['x','y']
#     else :
#       col_variable=['x','z']

#     for i in timestamp:
#         frame = filter_data[filter_data['timestamps']== i]
#         dbscan_data=frame[col_variable].values.astype('float32',copy=False)
#         model = DBSCAN(eps=eps_value, min_samples=2, metric='euclidean').fit(dbscan_data)
#         labels=model.labels_
#         color_list.extend(labels)

#         # Number of clusters in labels, ignoring noise if present.
#         n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#         n_clusters_list.append(n_clusters_)
#         n_noise_list.append( list(labels).count(-1))

#         if n_clusters_ >= 2:
#             target_1=frame[model.labels_ == 0]
#             target_2=frame[model.labels_ == 1]

#             if target_1[test].mean()<target_2[test].mean():
#                 l_target = target_1
#                 r_target = target_2
#             else:
#                 l_target = target_2
#                 r_target = target_1

#             c_point.append(0)
#             sepration_angle.append((abs(target_1[test].mean()-target_2[test].mean()))*180/np.pi)
            
#             l_target_rcs.append(l_target['power'].mean())
#             r_target_rcs.append(r_target['power'].mean())
#             l_point.append(len(l_target))
#             r_point.append(len(r_target))
            
#         else:
#             target_c=frame[model.labels_ == 0]
#             sepration_angle.append(0)
#             center_pos_rcs.append(target_c['power'].mean())
#             l_point.append(0)
#             r_point.append(0)
#             c_point.append(len(target_c))
#     if len( center_pos_rcs)==0:
#        center_pos_rcs =[0]
#     if len( l_target_rcs )==0:
#       l_target_rcs = [0] 
#     if len( r_target_rcs )==0:
#       r_target_rcs = [0] 
#     return frame,labels,n_clusters_list,sepration_angle,timestamp,l_target_rcs,center_pos_rcs, r_target_rcs,l_point,r_point,c_point,color_list