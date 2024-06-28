#2024-05-18. This code calculates randomly chooses one of the optitum trajectories between two points in a lattice of NxN nodes (equivalent to air zones)

import numpy as np
import random as rnd
import copy
import pandas as pd

import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


#Size of lattice; origin and destination; minimum distance between origin and destination; keep the trajectory with a list of nodes
#---------------------------------
planes=1 #number of planes
N=3
ori=np.array([0,0]);des=np.array([2,2])
d=sum(abs(ori - des)) #distance origin destination
trajectories = [list(ori)]
#---------------------------------

print("starting at:", ori, ". Destination:", des, ". Minimum distance:", d)

                    #left,             up,              right,           down
translate=[np.array([0,-1]), np.array([-1,0]), np.array([0,1]), np.array([1,0])]


while d > 0:
    new_ori = ori + rnd.choice(translate)    #Observe that being out of the lattice is also a candidate, but it will always be a bad candidate
    new_d = sum(abs(new_ori - des))
    if new_d < d:
        ori = new_ori
        d = new_d
        trajectories.append(list(ori))
    
print(trajectories)

#Save trajectories to dataframe and dataframe to csv
#---------------------------------
x_move=[step[0] for step in trajectories]
y_move=[step[1] for step in trajectories]

d_tr = pd.DataFrame({'plane_1_x' : x_move, 'plane_1_y': y_move})
d_tr.to_csv('../data/' + 'trajectories_size_' + str(N) + '_planes_' + str(planes)+  '.csv')
#---------------------------------
