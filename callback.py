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
        if label != None:
            label.config(text=file)
    else:  # user cancel the file browser window
        print("No file chosen")


def main_column(main_column_entry):
    '''The inputs are the number seprated by ',' conatin orignal data frame coloumn in order to
    [timestamp, Azimuth, Elevation, range, rangerate, power ]

    example: orignal data frame coloum name -> [timestamp, Elevation, Azimuth, rangerate, power, range, x, y, z]
    input would be 1,3,2,6,4,5

    This help to rearrange the coloumn and remove the extra coloumn 
    We needed this arrangement because the data columns differ from company to company.
    '''
    col_number = main_column_entry.get().split(",")
    col_number = list(map(int, col_number))
    col_list = list(data.columns)

    # -----------------------------Main data re-arrangement------------------------------------------#
    global main_data
    main_data = data[[col_list[col_number[0]],
                      col_list[col_number[3]], col_list[col_number[4]], col_list[col_number[5]]]]

    # Check whether the angles in the data are degrees or radians 
    # If the data is in degrees we need to convert it to radians, the method "isdeg" will check and convert the angle.
    main_data.insert(1, "Azimuth", isdeg(data[col_list[col_number[1]]]))
    main_data.insert(2, "Elevation", isdeg(data[col_list[col_number[2]]]))
    cols = ['timestamps', "Azimuth", "Elevation",
            "range", "rangerate", "power"]    
    main_data.columns = cols # define the coloumn haders
    main_data = ploar2xyz(main_data) # convert polor to xyz co-ordinate

    # -----------------------------Define Global Filter data------------------------------------------#
    # define filter data (this data will use as main data frame in the code)
    global filter_data  
    filter_data = main_data.copy()
    print(main_data)


def reset_filter():
    ''' Reset the applied filter and make data back to orignal'''
    global filter_data
    filter_data = main_data.copy()
    print(filter_data)


def apply_filter(max_val, min_val, filter_Name):
    '''This method applies the filter threshold to the data value.'''

    if max_val.get() != "" and min_val.get() != "":
        if float(max_val.get()) < float(min_val.get()):
            max_val.config(fg="red")
            min_val.config(fg="red")
            return 0
    max_val.config(fg="black")
    min_val.config(fg="black")
    global filter_data
    filter_data = filter(filter_data, filter_Name, 
                         min_val.get(), max_val.get())  
    print(filter_data)


def plot(root):
    ''' This method plot all the informative graph on the main GUI screen'''

    fig = polar_view(
        filter_data['Azimuth'], filter_data['range'], max_theta=70, min_theta=-70)
    fig_bird_eye = plot_bird_eye(filter_data, lable=[])
    fig_plot3d = plot3d(filter_data)
    fig_vel = vel_plot(filter_data)
    fig_power_prob_dens = plot_prob_dens(filter_data['power'], "Power")
    fig_vel_prob_dens = plot_prob_dens(filter_data['rangerate'], "Velocity")
    fig_bird_eye2 = plot_bird_eye(filter_data, lable=[],parameter=["y", "z"])

    # embedded fig on GUI
    canvas = FigureCanvasTkAgg(fig,master=root)                              
    canvas_bird_eye = FigureCanvasTkAgg(fig_bird_eye,master=root)                                       
    canvas_bird_eye2 = FigureCanvasTkAgg(fig_bird_eye2,master=root)                                        
    fig_plot3d = FigureCanvasTkAgg(fig_plot3d,master=root)                                   
    canvas_vel = FigureCanvasTkAgg(fig_vel,master=root)                                   
    canvas_power_prob_dens = FigureCanvasTkAgg(fig_power_prob_dens,master=root)                                              
    canvas_vel_prob_dens = FigureCanvasTkAgg(fig_vel_prob_dens,master=root)
                                             
    # Dwaring on canvas
    canvas.draw()
    canvas_bird_eye.draw()
    canvas_bird_eye2.draw()
    fig_plot3d.draw()
    canvas_vel.draw()
    canvas_power_prob_dens.draw()
    canvas_vel_prob_dens.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=-18, y=450)
    canvas_bird_eye.get_tk_widget().place(x=765, y=50)
    canvas_bird_eye2.get_tk_widget().place(x=360, y=50)
    fig_plot3d.get_tk_widget().place(x=1155, y=50)
    canvas_vel.get_tk_widget().place(x=360, y=450)
    canvas_vel_prob_dens.get_tk_widget().place(x=765, y=450)
    canvas_power_prob_dens.get_tk_widget().place(x=1150, y=450)
    plt.close('all') 


def algo(root, variable, eps_entry=None, thershold_wall_max_entry=None,
         thershold_wall_min_entry=None):

    test = variable.get()
    if test == "Azimuth" or test == "Elevation":

        if test == "Azimuth":
            parameter_column = "y"
        else:
            parameter_column = "z"

        if thershold_wall_max_entry.get() == "":
            thershold_wall_max = filter_data[parameter_column].mean() + 0.05
        if thershold_wall_min_entry.get() == "":
            thershold_wall_min = filter_data[parameter_column].mean() - 0.05
        if thershold_wall_max_entry.get() != "" and thershold_wall_min_entry.get() != "":
            if float(thershold_wall_max_entry.get()) < float(thershold_wall_min_entry.get()):
                thershold_wall_max_entry.config(fg="red")
                thershold_wall_min_entry.config(fg="red")
                return 0
            thershold_wall_max_entry.config(fg="black")
            thershold_wall_min_entry.config(fg="black")
            thershold_wall_min = float(thershold_wall_min_entry.get())
            thershold_wall_max = float(thershold_wall_max_entry.get())
        

        res = sep_algo(filter_data, test, thershold_wall_min,
                       thershold_wall_max, eps_entry)

        fig1 = polar_view(filter_data[test], filter_data['range'],
                          max_theta=70, min_theta=-70, Color=res["color_labels"])

        if test == 'Elevation':
            fig2 = plot_bird_eye(
                filter_data, lable=res["color_labels"], Color=res["color_labels"], parameter=["y", "z"])
        else:
            fig2 = plot_bird_eye(
                filter_data, lable=res["color_labels"],  Color=res["color_labels"])

        fig4 = plot_sep_info(res['timestamp'], res['sepration_angle'])
        fig3 = plot_point_stat(res['timestamp'], res['left_point'], res['right_point'], res['mean_pose_point'])
        sepration_angle = [i for i in res['sepration_angle'] if i != 0]
        fig5 = plot_prob_dens(sepration_angle, "Sepration Angle")
        fig6 = plot_violin([res['left_target_rcs'], res['mean_pose_rcs'], res['right_target_rcs']])
        fig7 = plot_sepration_percentage_info(res['percentage'])

        # embedded fig on GUI
        canvas1 = FigureCanvasTkAgg(fig1,master=root)                                  
        canvas2 = FigureCanvasTkAgg(fig2,master=root)                                 
        canvas3 = FigureCanvasTkAgg(fig3,master=root)                                 
        canvas4 = FigureCanvasTkAgg(fig4,master=root)                                    
        canvas5 = FigureCanvasTkAgg(fig5,master=root)                                   
        canvas6 = FigureCanvasTkAgg(fig6,master=root)                                    
        canvas7 = FigureCanvasTkAgg(fig7,master=root)

        # Dwaring on canvas
        canvas1.draw()
        canvas2.draw()
        canvas3.draw()
        canvas4.draw()
        canvas5.draw()
        canvas6.draw()
        canvas7.draw()

        # # placing the canvas on the Tkinter window
        canvas1.get_tk_widget().place(x=-18, y=450)
        canvas2.get_tk_widget().place(x=765, y=50)
        canvas3.get_tk_widget().place(x=1152, y=50)
        canvas4.get_tk_widget().place(x=360, y=450)
        canvas5.get_tk_widget().place(x=765, y=450)
        canvas6.get_tk_widget().place(x=1152, y=450)
        canvas7.get_tk_widget().place(x=360, y=50)
    else:
        print("under development")
    plt.close('all')


def selected_choice(test_name):
    global test
    test = test_name.get()
    print(test)


def save_file(root):
    try:
        file = filedialog.asksaveasfilename(filetypes=[("csv file", ".csv")],
                                            defaultextension=".csv")
        if file:
            filter_data.to_csv(file, index=False)
    except AttributeError:
        # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
        print("The user cancelled save")
