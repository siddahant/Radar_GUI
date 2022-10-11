from tkinter import filedialog
import pandas as pd 
from tkinter import Entry
import matplotlib.pyplot as plt
from method import *
from plot_utility import *
from sklearn.metrics import silhouette_score


def upload_file(label=None):
    '''This Method allow user to import the .txt and csv file by clicking the Upload file button '''

    f_types = [('CSV files', "*.csv"),
                ('Text Document', '*.txt')]
    file = filedialog.askopenfilename(
        filetypes=f_types)

    if file:  # user selected one file
        global data
        data = pd.read_csv(file)
        if label!=None:
            label.config(text=file)
    else:  # user cancel the file browser window
        print("No file chosen")


def main_column(main_column_entry):
    '''The input is a list conatin orignal data frame coloumn in order to
    [timestamp, Azimuth, Elevation, range, rangerate, power ]

    example: orignal data frame coloum name -> [datae, timestamps in, timestamps out, azimuth, rcs, elevation, rangerate, range,]
    input would be [1,3,5,7,6,4] 
    
    This help to rearrange the coloumn and remove the extra coloumn
    '''
    col_number =  main_column_entry.get().split(",")
    col_number = list(map(int, col_number))
    col_list = list(data.columns)
    global main_data
    main_data = data[[ col_list[col_number[0]],
              col_list[col_number[3]], col_list[col_number[4]], col_list[col_number[5]] ]]

    main_data.insert(1, "Azimuth",isdeg(data[col_list[col_number[1]]]))
    main_data.insert(2, "Elevation",isdeg(data[col_list[col_number[2]]]))

    cols = ['timestamps', "Azimuth", "Elevation", "range", "rangerate", "power" ]
    main_data.columns = cols
    main_data=ploar2xyz(main_data)
    global filter_data
    filter_data = main_data.copy()
    print(main_data)


def reset_filter():
    global filter_data
    filter_data = main_data.copy()
    print(filter_data)

def apply_filter(max_val,min_val,filter_Name):
    
    if max_val.get() !="" and min_val.get() !="":
        if float(max_val.get())<float(min_val.get()):
            max_val.config(fg= "red")
            min_val.config(fg= "red")
            return 0
    max_val.config(fg= "black")
    min_val.config(fg= "black")    
    global filter_data
    filter_data = filter(filter_data,filter_Name,min_val.get(), max_val.get())
    print(filter_data)


def plot(root):     
    # define Figures
    fig=polar_view(filter_data['Azimuth'],filter_data['range'], max_theta=70, min_theta=-70)
    fig_bird_eye=plot_bird_eye(filter_data, lable = [])
    fig_plot3d=plot3d(filter_data)
    fig_vel= vel_plot(filter_data)
    fig_power_prob_dens=plot_prob_dens(filter_data['power'],"Power")
    fig_vel_prob_dens=plot_prob_dens(filter_data['rangerate'],"Velocity")


    # embedded fig on GUI
    canvas = FigureCanvasTkAgg(fig,
                               master = root)
    canvas_bird_eye = FigureCanvasTkAgg(fig_bird_eye,
                               master = root)  
    fig_plot3d = FigureCanvasTkAgg(fig_plot3d,
                               master = root) 

    canvas_vel = FigureCanvasTkAgg(fig_vel,
                               master = root) 
    canvas_power_prob_dens = FigureCanvasTkAgg(fig_power_prob_dens,
                                master = root)
    canvas_vel_prob_dens = FigureCanvasTkAgg(fig_vel_prob_dens,
                                master = root)

                                 
    # Dwaring on canvas 
    canvas.draw()
    canvas_bird_eye.draw()
    fig_plot3d.draw()
    canvas_vel.draw()
    canvas_power_prob_dens.draw()
    canvas_vel_prob_dens.draw()

    # # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=360,y=-100)
    canvas_bird_eye.get_tk_widget().place(x=765,y=0)
    fig_plot3d.get_tk_widget().place(x=1155,y=0)
    canvas_vel.get_tk_widget().place(x=360,y=350)
    canvas_vel_prob_dens.get_tk_widget().place(x=765,y=350)
    canvas_power_prob_dens.get_tk_widget().place(x=1150,y=350)
    plt.close('all')


def algo(root,eps_value):

    if eps_value.get()=="":
        eps_value=0.2
    else:
        eps_value = float(eps_value.get())
    timestamp = filter_data.timestamps.unique()
    azimuth_sepration = []
    silhouette_coeff = []
    l_target_rcs = [] 
    r_target_rcs = []
    center_pos_rcs =[]
    r_point=[]
    l_point=[]
    c_point=[]
    n_clusters_list=[]
    n_noise_list=[]
    color_list=[]
    for i in timestamp:
        frame = filter_data[filter_data['timestamps']== i]
        dbscan_data=frame[['x','y']].values.astype('float32',copy=False)
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

            if target_1['Azimuth'].mean()<target_2['Azimuth'].mean():
                l_target = target_1
                r_target = target_2
            else:
                l_target = target_2
                r_target = target_1

            c_point.append(0)
            center_pos_rcs.append(0)
            azimuth_sepration.append((abs(target_1['Azimuth'].mean()-target_2['Azimuth'].mean()))*180/np.pi)
            silhouette_coeff.append((silhouette_score(dbscan_data, labels)))
            
            l_target_rcs.append(l_target['power'].mean())
            r_target_rcs.append(r_target['power'].mean())
            l_point.append(len(l_target))
            r_point.append(len(r_target))
            
        else:
            target_c=frame[model.labels_ == 0]
            azimuth_sepration.append(0)
            silhouette_coeff.append(0)
            l_target_rcs.append(0)
            r_target_rcs.append(0)
            center_pos_rcs.append(target_c['power'].mean())
            l_point.append(0)
            r_point.append(0)
            c_point.append(len(target_c))



    # define Figures
    fig=polar_view(filter_data['Azimuth'],filter_data['range'], max_theta=70, min_theta=-70,Color=color_list)
    fig_bird_eye=plot_bird_eye(frame, lable = labels, Color=labels)

    fig_prob_dens=plot_prob_dens(azimuth_sepration,"Sepration Angle")
    fig_sep_info= plot_sep_info(timestamp,azimuth_sepration,n_clusters_list)

    fig_point_stat = plot_point_stat(timestamp,l_point,r_point,c_point)
    fig_plot_violin = plot_violin([l_target_rcs,center_pos_rcs, r_target_rcs])


    # embedded fig on GUI
    canvas = FigureCanvasTkAgg(fig,
                               master = root)

    canvas_bird_eye = FigureCanvasTkAgg(fig_bird_eye,
                               master = root)  

    canvas_prob_dens= FigureCanvasTkAgg(fig_prob_dens,
                               master = root) 

    canvas_point_stat= FigureCanvasTkAgg(fig_point_stat,
                               master = root) 

    canvas_sep_info = FigureCanvasTkAgg(fig_sep_info,
                               master = root) 
    
    canvas_plot_violin = FigureCanvasTkAgg(fig_plot_violin,
                                master = root)


                                 
    # Dwaring on canvas 
    canvas.draw()
    canvas_bird_eye.draw()
    canvas_prob_dens.draw()
    canvas_point_stat.draw()
    canvas_sep_info.draw()
    canvas_plot_violin.draw()

    # # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=360,y=-100)
    canvas_bird_eye.get_tk_widget().place(x=765,y=0)
    canvas_point_stat.get_tk_widget().place(x=1152,y=0)

    canvas_prob_dens.get_tk_widget().place(x=765,y=350)
    canvas_sep_info.get_tk_widget().place(x=360,y=350)
    canvas_plot_violin.get_tk_widget().place(x=1152,y=350)

    plt.close('all')


def selected_choice(test_name):
    if test_name.get()=="static test":
        print(test_name.get())
    else:
        print("other")
        print(test_name.get())



def save_file(root):
    file = filedialog.asksaveasfilename(
        filetypes=[("csv file", ".csv")],
    defaultextension=".csv")
        