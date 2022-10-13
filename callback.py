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


def algo(root,eps_value,variable):
    test=(variable.get())
    if eps_value.get()=="":
        eps_value=0.2
    else:
        eps_value = float(eps_value.get())
    if test == "Azimuth" or test == "Elevation":

        frame,labels,n_clusters_list,sepration_angle,timestamp,l_target_rcs,center_pos_rcs, r_target_rcs,l_point,r_point,c_point,color_list = sep_algo(filter_data,eps_value,test)
        fig1=polar_view(filter_data[test],filter_data['range'], max_theta=70, min_theta=-70,Color=color_list)
        
        if test=='Elevation':
            fig2=plot_bird_eye(frame, lable = labels, Color=labels,parameter=["x","z"])
        else:
            fig2=plot_bird_eye(frame, lable = labels, Color=labels)

        fig4= plot_sep_info(timestamp,sepration_angle,n_clusters_list)
        fig3 = plot_point_stat(timestamp,l_point,r_point,c_point)
        fig5=plot_prob_dens(sepration_angle,"Sepration Angle")
        fig6= plot_violin([l_target_rcs,center_pos_rcs, r_target_rcs])

        # embedded fig on GUI
        canvas1 = FigureCanvasTkAgg(fig1,
                                master = root)

        canvas2 = FigureCanvasTkAgg(fig2,
                                master = root)  

        canvas3= FigureCanvasTkAgg(fig3,
                                master = root) 

        canvas4= FigureCanvasTkAgg(fig4,
                                master = root) 

        canvas5 = FigureCanvasTkAgg(fig5,
                                master = root) 
        
        canvas6 = FigureCanvasTkAgg(fig6,
                                    master = root)
                                
        # Dwaring on canvas 
        canvas1.draw()
        canvas2.draw()
        canvas3.draw()
        canvas4.draw()
        canvas5.draw()
        canvas6.draw()

        # # placing the canvas on the Tkinter window
        canvas1.get_tk_widget().place(x=360,y=-100)
        canvas2.get_tk_widget().place(x=765,y=0)
        canvas3.get_tk_widget().place(x=1152,y=0)

        canvas4.get_tk_widget().place(x=360,y=350)
        canvas5.get_tk_widget().place(x=765,y=350)
        canvas6.get_tk_widget().place(x=1152,y=350)

        plt.close('all')
    else:
        print("under development")


def selected_choice(test_name):
        global test
        test = test_name.get()
        print(test)





def save_file(root):
    file = filedialog.asksaveasfilename(
        filetypes=[("csv file", ".csv")],
    defaultextension=".csv")
        