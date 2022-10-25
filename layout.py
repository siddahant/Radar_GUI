from logging import RootLogger
from tkinter import *
from turtle import width
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
                            width=20, command=lambda: upload_file(upload_label), fg="blue")
# selecting main coloums
'''This buttom allow to filter the main columns and arrange the data frame'''
main_column_button = Button(root, text='Main columns',
                            width=20, command=lambda: [main_column(main_column_entry), plot(root)], fg="blue")

reset_filter_button = Button(root, text='Reset Filter',
                             width=20, command=lambda: [reset_filter(), plot(root)], fg="blue")

frame_filter_button = Button(root, text='Timestamp Filter',
                             width=20, command=lambda: [apply_filter(frame_max_entry, frame_min_entry, 'T'), plot(root)], fg="blue")

azimuth_filter_button = Button(root, text='Azimuth Filter',
                               width=20, command=lambda: [apply_filter(azimuth_max_entry, azimuth_min_entry, 'A'), plot(root)], fg="blue")

elevation_filter_button = Button(root, text='Elevation Filter',
                                 width=20, command=lambda: [apply_filter(elevation_max_entry, elevation_min_entry, 'E'), plot(root)], fg="blue")

vel_filter_button = Button(root, text='Velocity Filter',
                           width=20, command=lambda: [apply_filter(vel_max_entry, vel_min_entry, 'V'), plot(root)], fg="blue")

range_filter_button = Button(root, text='Range Filter',
                             width=20, command=lambda: [apply_filter(range_max_entry, range_min_entry, 'R'), plot(root)], fg="blue")

power_filter_button = Button(root, text='Power Filter',
                             width=20, command=lambda: [apply_filter(power_max_entry, power_min_entry, 'P'), plot(root)], fg="blue")

x_filter_button = Button(root, text='X Filter',
                         width=20, command=lambda: [apply_filter(x_max_entry, x_min_entry, 'X'), plot(root)], fg="blue")

y_filter_button = Button(root, text='Y Filter',
                         width=20, command=lambda: [apply_filter(y_max_entry, y_min_entry, 'Y'), plot(root)], fg="blue")

z_filter_button = Button(root, text='Z Filter',
                         width=20, command=lambda: [apply_filter(z_max_entry, z_min_entry, 'Z'), plot(root)], fg="blue")
run_algo_button = Button(root, text='Run',
                         width=20, command=lambda: [algo(root, variable, eps_entry,
                                                         thershold_wall_max_entery,
                                                         thershold_wall_min_entery)], fg="green")

Save_filter_data_button = Button(root, text='Save filter_data',
                                 width=20, command=lambda: save_file(root), fg="blue")


###############################################################################
#                               Entery                                        #
###############################################################################


main_column_entry = Entry(root, width=10)

frame_max_entry = Entry(root, width=5)
frame_min_entry = Entry(root, width=5)

azimuth_max_entry = Entry(root, width=5)
azimuth_min_entry = Entry(root, width=5)

elevation_max_entry = Entry(root, width=5)
elevation_min_entry = Entry(root, width=5)

vel_max_entry = Entry(root, width=5)
vel_min_entry = Entry(root, width=5)

range_max_entry = Entry(root, width=5)
range_min_entry = Entry(root, width=5)

power_max_entry = Entry(root, width=5)
power_min_entry = Entry(root, width=5)

x_max_entry = Entry(root, width=5)
x_min_entry = Entry(root, width=5)
y_max_entry = Entry(root, width=5)
y_min_entry = Entry(root, width=5)
z_max_entry = Entry(root, width=5)
z_min_entry = Entry(root, width=5)

eps_entry = Entry(root, width=5)

thershold_wall_max_entery = Entry(root, width=5)
thershold_wall_min_entery = Entry(root, width=5)


###############################################################################
#                               labels                                        #
###############################################################################

# data file handels labels
upload_label = Label(root, text="", font=my_font, width=10)

# filter labels
max_label = Label(root, text='MAX Value',  font=my_font, width=10)
min_label = Label(root, text='MIN Value',  font=my_font, width=10)
eps_label = Label(root, text='Eps Value', width=10)
thershold_wall_label = Label(root, text='Thershold wall', width=10)

###############################################################################
#                            dropdown                                         #
###############################################################################
option = ["Azimuth", "Elevation", "Car test", "Pedestrian test"]
variable = StringVar()
variable.set(option[0])
dropdown = OptionMenu(root, variable, *option)

dropdown.config(width=18)

###############################################################################
#                            Locations                                        #
###############################################################################

# data file handels loactions
file_upload_button.grid(row=0, column=0, columnspan=1)
main_column_button.grid(row=1, column=0, columnspan=1)
main_column_entry.grid(row=1, column=1)
upload_label.grid(row=0, column=1)

min_label.grid(row=2, column=1)
max_label.grid(row=2, column=2)

frame_filter_button.grid(row=3, column=0)
frame_min_entry.grid(row=3, column=1)
frame_max_entry.grid(row=3, column=2)

azimuth_filter_button.grid(row=4, column=0)
azimuth_min_entry.grid(row=4, column=1)
azimuth_max_entry.grid(row=4, column=2)

elevation_filter_button.grid(row=5, column=0)
elevation_min_entry.grid(row=5, column=1)
elevation_max_entry.grid(row=5, column=2)

range_filter_button.grid(row=6, column=0)
range_min_entry.grid(row=6, column=1)
range_max_entry.grid(row=6, column=2)

vel_filter_button.grid(row=7, column=0)
vel_min_entry.grid(row=7, column=1)
vel_max_entry.grid(row=7, column=2)

power_filter_button.grid(row=8, column=0)
power_min_entry.grid(row=8, column=1)
power_max_entry.grid(row=8, column=2)


x_filter_button.grid(row=9, column=0)
x_min_entry.grid(row=9, column=1)
x_max_entry.grid(row=9, column=2)

y_filter_button.grid(row=10, column=0)
y_min_entry.grid(row=10, column=1)
y_max_entry.grid(row=10, column=2)

z_filter_button.grid(row=11, column=0)
z_min_entry.grid(row=11, column=1)
z_max_entry.grid(row=11, column=2)

reset_filter_button.grid(row=12, column=1, columnspan=2)
dropdown.grid(row=12, column=0, columnspan=1)

thershold_wall_max_entery.grid(row=13, column=2)
thershold_wall_min_entery.grid(row=13, column=1)
thershold_wall_label.grid(row=13, column=0)

eps_entry.grid(row=14, column=1)
eps_label.grid(row=14, column=0)

Save_filter_data_button.grid(row=15, column=0)
run_algo_button.grid(row=15, column=1, columnspan=2)
