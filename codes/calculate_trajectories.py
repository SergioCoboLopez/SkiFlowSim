#2024-05-16. This code calculates all possible trajectories between two points in a lattice of NxN nodes (equivalent to air zones)

import numpy as np
import random
import copy

import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.animation as animation


#Size of lattice, origin and destination
#---------------------------------
N=3
ori=[0,0];des=[2,2]
#---------------------------------

#Max steps in a trajectory and number of trajectories
#---------------------------------
max_steps=10;max_trajectories=10
trajectories=[]
#---------------------------------

print("starting at:", ori, ". Destination:", des)

          #0: left,   1: up,     2: right, 3: down
translate={0: [0,-1], 1: [-1,0], 2: [0,1], 3: [1,0]}
opposite={0:2, 1:3, 2:0, 3:1} #opposite directions 

for iteration in range(max_trajectories):
    probabilities=[0, 0, 0.5, 0.5] #probabilities of numbers being selected
    
    pos_0=copy.copy(ori) #Initial position
    pos_t=copy.copy(pos_0) #Position of plane at time t
    trajectory=[pos_0]   #Initialize trajectory
    
    
    for step in range(max_steps):
        #Generate directions at random from uniform distribution
        #0: left, 1: up, 2: right, 3: down
        where = np.random.choice(4,1, p=probabilities)[0]

        #Translate number to actual direction
        to = translate[where]

        #Needs to be finished
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        reverse = opposite[where] #index of forbidden movement
        #Add whatever code needed to prevent the plane from going
        #backwards
        #Simply setting the probability to zero does not work.
        #Whatever the original p(reverse), you need to uniformly
        #distribute that probability among the other probabilities
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        #Update position
        pos_t=[sum(x) for x in zip(pos_t, to)]

        #Stop if destination is reached
        if pos_t==des:
            print("success!")
            trajectory.append(des)
            break
        
        #Set constrains for corners
        if pos_t==[0,0]:
            probabilities=[0, 0, 0.5, 0.5]
        elif pos_t==[N-1,N-1]:
            probabilities=[0.5, 0.5, 0, 0]
        elif pos_t==[0,N-1]:
            probabilities=[0.5, 0, 0, 0.5]
        elif pos_t==[N-1,0]:
            probabilities=[0, 0.5, 0.5, 0]

        #Set constrains for boundaries
        elif pos_t[1]==N-1:
            probabilities=[1/3, 1/3, 0, 1/3]
        elif pos_t[1]==0:
            probabilities=[0, 1/3, 1/3, 1/3]
        elif pos_t[0]==0:
            probabilities=[1/3, 0, 1/3, 1/3]
        elif pos_t[0]==N-1:
            probabilities=[1/3, 1/3, 1/3, 0]
            
            
        where_b=where          #Save past move 
        pos_b=copy.copy(pos_t) #Save past position

        trajectory.append(pos_b) #Store in list
        
    trajectories.append(trajectory)#Store trajectory in list of lists

    
print(trajectories)

#Plot one trajectory
#---------------------------------
lattice=[ [x,y] for x in range(N) for y in range(N)]
print(lattice)
x_lattice=[step[0] for step in lattice]
y_lattice=[step[1] for step in lattice]

x_move=[step[0] for step in trajectories[1]]
y_move=[step[1] for step in trajectories[1]]


#Define figure size in cm
cm = 1/2.54 #convert inch to cm
width = 8*cm; height=4*cm 

#Figure settings                                                     
#--------------------------------
output_path='../results/plots/' #A path to save figure
extensions=['.svg','.png','.pdf']     #Extensions to save figure

#Define figure size                                                  
cm = 1/2.54 #convert inch to cm                                      
width = 8*cm; height=4*cm #8x4cm for each figure in panel

#Fonts and sizes                                                     
size_axis=7;size_ticks=6;size_title=5
line_w=1;marker_s=3
#--------------------------------

#Plots                                                               
#--------------------------------
for i in range(len(x_move)-1):
    plt.arrow(x_move[i], y_move[i], (x_move[i+1]-x_move[i])*0.3, (y_move[i+1]-y_move[i])*0.3,width=0.01,color='r')
    plt.text(x_move[i] + 0.05, y_move[i]+0.05, 'step ' + str(i), fontsize= size_axis)

plt.plot(x_move,y_move,color='red',linestyle='dotted')

plt.scatter(x_lattice[:-1], y_lattice[:-1])
plt.scatter(ori[0], ori[1], color= 'r', marker='D')
plt.scatter(des[0], des[1], color= 'r', marker='*',s=100)


#Labels                                                              
plt.xlabel('x',fontsize=size_axis);plt.ylabel('y',fontsize=size_axis)

#Ticks                                                               
xtick_labels=[0, 1, 2 ]
plt.xticks(xtick_labels, fontsize=size_ticks)

ytick_labels=[0, 1, 2 ]
plt.yticks(ytick_labels, fontsize=size_ticks)

#legend                                                              
#plt.legend(loc='best',fontsize=size_ticks,frameon=False)

name_fig='trajectory'
#save fig                                                            
for ext in extensions:
    plt.savefig(output_path+name_fig+ext,dpi=300)

plt.show()
#-------------------------------- 



fig, ax = plt.subplots()
t = np.linspace(0, 3, 40)
g = -9.81
v0 = 12
z = g * t**2 / 2 + v0 * t

v02 = 5
z2 = g * t**2 / 2 + v02 * t

scat = ax.scatter(t[0], z[0], c="b", s=5, label=f'v0 = {v0} m/s')
line2 = ax.plot(t[0], z2[0], label=f'v0 = {v02} m/s')[0]
ax.set(xlim=[0, 3], ylim=[-4, 10], xlabel='Time [s]', ylabel='Z [m]')
ax.legend()


def update(frame):
    # for each frame, update the data stored on each artist.
    x = t[:frame]
    y = z[:frame]
    # update the scatter plot:
    data = np.stack([x, y]).T
    scat.set_offsets(data)
    # update the line plot:
    line2.set_xdata(t[:frame])
    line2.set_ydata(z2[:frame])
    return (scat, line2)


ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)
plt.show()
