import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd

#Data 
#--------------------------------

N=3;planes=1
d=pd.read_csv('../data/trajectories_size_'+ str(N) + '_planes_' + str(planes) + '.csv')

print(d)
#--------------------------------                                   


#Figure settings
output_path='../results/plots/' #A path to save figure
name_fig='trajectory_' + str(N) + '_planes_' + str(planes)
extensions=['.svg','.png','.pdf']     #Extensions to save figure

#Define figure size in cm
cm = 1/2.54 #convert inch to cm
width = 8*cm; height=4*cm 


#Figure settings                                                     
#--------------------------------                                    
#Define figure size                                                  
cm = 1/2.54 #convert inch to cm                                      
width = 8*cm; height=4*cm #8x4cm for each figure in panel

#Fonts and sizes                                                     
size_axis=7;size_ticks=6;size_title=5
line_w=1;marker_s=3
#--------------------------------

#Plots                                                               
#--------------------------------                                    
line_w=1;marker_s=3 #width and marker size

lattice=[ [x,y] for x in range(N) for y in range(N)]
x_lattice=[step[0] for step in lattice]
y_lattice=[step[1] for step in lattice]

print(d.plane_1_x)

plt.plot(d.plane_1_x,d.plane_1_y,color='red',linestyle='dotted')

ori_x=d.plane_1_x.iloc[0];ori_y=d.plane_1_y.iloc[0]
des_x=d.plane_1_x.iloc[-1];des_y=d.plane_1_y.iloc[-1]
plt.scatter(x_lattice[:-1], y_lattice[:-1])
plt.scatter(ori_x, ori_y, color= 'r', marker='D')
plt.scatter(des_x, des_y, color= 'r', marker='D')

for i in range(len(d.plane_1_x)-1):
    plt.arrow(d.plane_1_x[i], d.plane_1_y[i], (d.plane_1_x[i+1]-d.plane_1_x[i])*0.3, (d.plane_1_y[i+1]-d.plane_1_y[i])*0.3,width=\
0.01,color='r')
    plt.text(d.plane_1_x[i] + 0.05, d.plane_1_y[i]+0.05, 'step ' + str(i), fontsize= size_axis)

#Labels                                                              
plt.xlabel('x',fontsize=size_axis);plt.ylabel('y',fontsize=size_axis)

#Ticks                                                                                              
xtick_labels=range(N)
plt.xticks(xtick_labels, fontsize=size_ticks)

ytick_labels=range(N)
plt.yticks(ytick_labels, fontsize=size_ticks)

#save fig                                                            
for ext in extensions:
    plt.savefig(output_path+name_fig+ext,dpi=300)

plt.show()
#-------------------------------- 
