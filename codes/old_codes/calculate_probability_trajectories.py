#2024-05-16. This code calculates all possible trajectories between two points in a lattice of NxN nodes (equivalent to air zones)

import numpy as np
import random
import copy

import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd


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

#Save trajectories to dataframe and dataframe to csv
#---------------------------------
x_move=[step[0] for step in trajectories[0]]
y_move=[step[1] for step in trajectories[0]]

d_tr=pd.DataFrame({'plane_0_x' : x_move, 'plane_0_y' : y_move})

i=1
for trajectory in trajectories[1:]:
    x_move=[step[0] for step in trajectory]
    y_move=[step[1] for step in trajectory]
    d_tr_i=pd.DataFrame({'plane_'+str(i)+'_x' : x_move, 'plane_'+str(i)+'_y' : y_move})

    d_tr=pd.concat([d_tr, d_tr_i],axis=1)
    i+=1
    
d_tr.to_csv('../data/' + 'probability_trajectories_size_' + str(N) +   '.csv')
#---------------------------------
