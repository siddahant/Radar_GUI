import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from collections import Counter
from sklearn.cluster import DBSCAN


def ploar2xyz(df):
    '''Convert polar cordinate to xyz cordinate
    '''
    x = df['range'] * np.cos(df['Elevation']) * np.cos(df['Azimuth'])
    y = df['range'] * np.cos(df['Elevation']) * np.sin(df['Azimuth'])
    z = df['range'] * np.sin(df['Elevation'])
    df.insert(6, "x", x, True)
    df.insert(7, "y", y, True)
    df.insert(8, "z", z, True)
    return df


def isdeg(angle):
    '''convert the degree into radian if the given data is in degree'''
    if max(angle) > 1.57079028204:
        return angle*np.pi/180
    return angle


def filter(df, filter_Name, min_val="", max_val=""):
    filters = {"A": "Azimuth",
               "E": "Elevation",
               "V": "rangerate",
               "R": "range",
               "P": 'power',
               "X": "x",
               "Y": "y",
               "Z": "z",
               "T": "timestamps"}

    if min_val == "":
        min_val = min(df[filters[filter_Name]])
    if max_val == "":
        max_val = max(df[filters[filter_Name]])

    if (filter_Name == "A" or filter_Name == "E") and min_val != "":
        min_val = float(min_val)*np.pi/180

    if (filter_Name == "A" or filter_Name == "E") and max_val != "":
        max_val = float(max_val)*np.pi/180

    return df[(df[filters[filter_Name]] >= float(min_val)) & (df[filters[filter_Name]] <= float(max_val))]


def get_sepration_info(targets):
    sepration_list = []
    for i in targets:
        if len(i) == 3:
            sepration_list.append("p")
        elif len(i) == 1:
            if "l" in i or "r" in i:
                sepration_list.append("b")
            else:
                sepration_list.append("m")
        elif ("l" in i) and ("r" in i):
            sepration_list.append("s")
    sepration_percentage = (sepration_list.count('s')/len(sepration_list))*100
    blink_percentage = (sepration_list.count('b')/len(sepration_list))*100
    mean_pose_percentage = (sepration_list.count('m')/len(sepration_list))*100
    partial_sepration_percentage = (
        sepration_list.count('p')/len(sepration_list))*100
    percentage = {"separated": sepration_percentage,
                  "blink": blink_percentage,
                  "mean_pose": mean_pose_percentage,
                  "partial sepration": partial_sepration_percentage}
    return percentage


def run_dbscan(target_data,test,eps_entry):
    if test == "Elevation":
        col_variable = ['z', 'x']
    else:
        col_variable = ['x', 'y']

    dbscan_data = target_data[col_variable].values.astype(
        'float32', copy=False)

    if eps_entry.get() == "":
      eps_value = 0.1 
      search_one_cluster_eps_value = True
    else:
      eps_value = float(eps_entry.get())
      search_one_cluster_eps_value = False

    if dbscan_data.shape[0] > 1:
        if search_one_cluster_eps_value == False:
          model = DBSCAN(eps=eps_value, min_samples=2,
                           metric='euclidean').fit(dbscan_data)
          labels = model.labels_
          n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        else:
          incerase_eps_value = True
          while  incerase_eps_value:
              model = DBSCAN(eps=eps_value, min_samples=2,
                            metric='euclidean').fit(dbscan_data)
              labels = model.labels_
              n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
              if n_clusters_ == 1:
                  incerase_eps_value = False
              else:
                  eps_value = eps_value + eps_value*.5

    elif dbscan_data.shape[0] == 1:
        labels = np.array([0])
    else:
        labels = np.array([])
    return labels


def sep_algo(filter_data, test, thershold_wall_min, thershold_wall_max,eps_entry):
    temp_labels = []
    if test == "Azimuth":
        parameter = 'y'
    else:
        parameter = 'z'

    for xpos in filter_data[parameter]:
        if (thershold_wall_min > xpos) and (thershold_wall_max > xpos):
            temp_labels.append('l')
        elif (thershold_wall_min < xpos) and (thershold_wall_max < xpos):
            temp_labels.append('r')
        else:
            temp_labels.append('c')
    timestamp = filter_data.timestamps.unique()
    algo_data = filter_data.copy()
    algo_data.insert(9, "labels", temp_labels, allow_duplicates=False)
    left_target_rcs = []
    right_target_rcs = []
    mean_pose_rcs = []
    right_point = []
    left_point = []
    mean_pose_point = []
    sepration_angle = []
    targets = []
    color_labels = []
    for i in timestamp:
        target_detected = []
        frame = algo_data[algo_data['timestamps'] == i]
        right_target_data = frame[frame['labels'] == 'r']
        right_target_labels = run_dbscan(right_target_data, test,eps_entry)
        frame.reset_index(inplace=True, drop=True)
        if len(right_target_labels) != 0:
            right_target_data = right_target_data[right_target_labels == 0]
            target_detected.append('r')
            right_target_rcs.append(right_target_data['power'].mean())
            right_point.append(len(right_target_data))
            color_list = (["r" if label == 0 else "k" for label in right_target_labels])
            j = 0
            for row in range(len(frame)):
                if frame.loc[row, 'labels'] == 'r':
                    frame.loc[row, 'labels'] = color_list[j]
                    j += 1
        else:
            right_point.append(0)

        left_target_data = frame[frame['labels'] == 'l']
        left_target_labels = run_dbscan(left_target_data, test,eps_entry)
        if len(left_target_labels) != 0:
            left_target_data = left_target_data[left_target_labels == 0]
            target_detected.append('l')
            left_target_rcs.append(left_target_data['power'].mean())
            left_point.append(len(left_target_data))
            color_list = (["b" if label == 0 else "k" for label in left_target_labels])
            j = 0
            for row in range(len(frame)):
                if frame.loc[row, 'labels'] == 'l':
                    frame.loc[row, 'labels'] = color_list[j]
                    j += 1
        else:
            left_point.append(0)

        if len(left_target_labels) != 0 and (len(right_target_labels) != 0):
            sepration_angle.append((abs(left_target_data['Azimuth'].mean(
            )-right_target_data['Azimuth'].mean()))*180/np.pi)
        else:
            sepration_angle.append(0)

        mean_pose_data = frame[frame['labels'] == 'c']
        mean_pose_labels = run_dbscan(mean_pose_data, test,eps_entry)
        if len(mean_pose_labels) != 0:
            mean_pose_data = mean_pose_data[mean_pose_labels == 0]
            target_detected.append('c')
            mean_pose_rcs.append(mean_pose_data['power'].mean())
            mean_pose_point.append(len(mean_pose_data))
            color_list = (["g" if label == 0 else "k" for label in mean_pose_labels])
            j = 0
            for row in range(len(frame)):
                if frame.loc[row, 'labels'] == 'c':
                    frame.loc[row, 'labels'] = color_list[j]
                    j += 1
        else:
            mean_pose_point.append(0)

        color_labels.extend(frame['labels'].tolist())
        targets.append(target_detected)

    if len(mean_pose_rcs) == 0:
        mean_pose_rcs = [0]
    if len(left_target_rcs) == 0:
        left_target_rcs = [0]
    if len(right_target_rcs) == 0:
        right_target_rcs = [0]

    percentage = get_sepration_info(targets)
    res = {"left_target_rcs": left_target_rcs,
           "right_target_rcs": right_target_rcs,
           "mean_pose_rcs": mean_pose_rcs,
           "right_point": right_point,
           "left_point": left_point,
           "mean_pose_point": mean_pose_point,
           "percentage": percentage,
           "timestamp": timestamp,
           "sepration_angle": sepration_angle,
           "color_labels": color_labels}
    return res