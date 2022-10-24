import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from scipy.stats import norm


def polar_view(theta, r, max_theta=360, min_theta=0,Color='r',Size=1):
  fig = plt.figure(figsize=(4, 4))
  ax = fig.add_subplot(projection='polar')
  ax.set_theta_zero_location("N")
  ax.set_theta_direction(-1)
  c = ax.scatter(theta, r, c=Color, s=Size)
  ax.set_thetamin(min_theta)
  ax.set_thetamax(max_theta)
  ax.set_rlim(0,max(r)+20)
#   plt.show()
  fig.tight_layout()
  return fig


def plot_bird_eye(df, lable = [], Color='r',parameter=None):
  if type(Color)==str:
    if Color=='r':
      Color=df["rangerate"]
  fig, ax= plt.subplots(figsize=(3.8, 3))
  if parameter==None:
    scatter = ax.scatter(data=df, x='y', y='x', c=Color,s=2)
    ax.set_ylabel("Y")
    ax.set_xlabel("X")
  else: 
    scatter = ax.scatter(data=df, x=parameter[0], y=parameter[1], c=Color,s=2)
    ax.set_ylabel(parameter[1])
    ax.set_xlabel(parameter[0])
  ax.set_title("Bird Eye View")
  if len(lable)==0:
    cbar = fig.colorbar(scatter)
    cbar.set_label('Velocity')
  else:
    # ax.legend(handles=scatter.legend_elements()[0], 
    #         labels=np.unique(lable).tolist(),
    #         title="Classes")
    pass
  # plt.show()
  fig.tight_layout()
  return fig
  

def plot_prob_dens(data,x_lable):

  # Fit a normal distribution to
  # the data:
  # mean and standard deviation


  mu, std = norm.fit(data) 
    
  # Plot the histogram.
  fig, ax= plt.subplots(figsize=(3.8, 3))
  ax.hist(data, bins=25, density=True, alpha=0.6, color='b')
    
  # Plot the PDF.
  xmin, xmax = plt.xlim()
  x = np.linspace(xmin, xmax, 100)
  p = norm.pdf(x, mu, std)
    
  ax.plot(x, p, 'k', linewidth=2)
  title = "Fit Values: {:.2f} and {:.2f}".format(mu, std)
  ax.set_xlabel(x_lable)
  ax.set_ylabel("probability density")
  ax.set_title(title)
  fig.tight_layout()
    
  # plt.show()
  return fig


def vel_plot(df):
  fig, ax= plt.subplots(figsize=(4, 3))
  scatter = ax.scatter(df['rangerate'],df['y'],c=df['power'],s=1)
  ax.set_xlabel("Y")
  ax.set_ylabel("Velocity")
  ax.set_title("Distance vs velocity graph")
  cbar = fig.colorbar(scatter)
  cbar.set_label('Power')
  fig.tight_layout()
  return fig
  # plt.show()

def plot3d(df):
  fig, ax= plt.subplots(figsize=(4, 3))
  ax = plt.axes(projection='3d')
  scatter= ax.scatter(df['x'],df['y'],df['z'],s=2,c='b')
  ax.set_xlabel("X")
  ax.set_ylabel("Y")
  ax.set_zlabel("Z")
  ax.set_title("3d point clouds")
  fig.tight_layout()
  return fig



def plot_point_stat(timestamp,l_point,r_point,c_point):
  fig, ax = plt.subplots(figsize=(4, 3))
  width=0.8
  ax.bar(timestamp, l_point, width, label='Left points')
  ax.bar(timestamp, r_point, width, bottom=l_point,
      label='Right points')
  ax.bar(timestamp,c_point,width,label='Mean Pos points')

  ax.set_ylabel('Number of Points')
  ax.set_xlabel('Frame Number')
  ax.set_title('Angular separation point')
  ax.legend()
  fig.tight_layout()
  return fig

def plot_sep_info(timestamp,azimuth_sepration):
  fig, ax1= plt.subplots(figsize=(4, 3))
  line=ax1.bar(timestamp,azimuth_sepration)
  # ax2.plot(timestamp,n_clusters_list,c='r')
  ax1.set_ylabel('Sepration Angle')
  ax1.set_xlabel('Frame Number')
  fig.tight_layout()
  return fig

def plot_violin(data):
  fig, ax = plt.subplots(figsize=(4, 3))
  ax.violinplot(data,
                  showmeans=False,
                  showmedians=True)
  ax.set_title('Violin plot')
  ax.yaxis.grid(True)
  ax.set_xticks([y + 1 for y in range(len(data))],
                  labels=['Left Target','Mean Pos', 'Right Target'])
  ax.set_ylabel('Observed RCS values')
  return fig
