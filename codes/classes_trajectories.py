#2024-05-18. This code calculates randomly chooses one of the optitum trajectories between two points in a lattice of NxN nodes (equivalent to air zones)

import numpy as np
import random as rnd
import copy
import pandas as pd

import matplotlib.gridspec as gridspec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

#-----------------------------------------------------
class grid:

    def __init__(self, N, M):
        self.matrix=np.zeros((N,M))

    #Initialize the matrix with the origins of all planes in the grid
    def initialize_transit(self, planes):
        for plane in planes:
            self.matrix[plane.origin[0], plane.origin[1]]+=1

    #Update positions of planes in grid
    def transit_state(self,planes):
        for plane in planes:
            self.matrix[plane.trajectory[-1][0], plane.trajectory[-1][1]]+=1
            self.matrix[plane.trajectory[-2][0], plane.trajectory[-2][1]]-=1
#-----------------------------------------------------

#Define the class "plane"
#-----------------------------------------------------
class plane:

    #Define Attributes of the class (its important characteristics)

    def __init__(self, ori_plane,des_plane):
        self.origin = np.array([ori_plane[0], ori_plane[1]]) #origin
        self.destin = np.array([des_plane[0], des_plane[1]]) #destination
        self.pos=self.origin                      #current position
        self.distance=sum(abs(self.pos-self.destin))#current distance to destination
        self.trajectory=[list(self.origin)]#current trajectory        
        

    #Methods: the things a plane does
    #move
    def update_pos_random(self, pos):
        movements = [np.array([0,-1]), np.array([-1,0]), np.array([0,1]), np.array([1,0])]
        
        proposed_pos  = self.pos + rnd.choice(movements)
        proposed_dist = sum(abs(proposed_pos - self.destin))

        self.pos = proposed_pos
        self.distance = proposed_dist
        self.trajectory.append(list(self.pos))


      #move
    def update_pos_optimally(self, pos):
        
        movements = [np.array([0,-1]), np.array([-1,0]), np.array([0,1]), np.array([1,0])]

        possible_positions=[self.pos + movement for movement in movements]
        possible_distances=[sum(abs(possible_position - self.destin)) for possible_position in possible_positions]
        
        min_distance=possible_distances.index(min(possible_distances))
        best_position=possible_positions[min_distance]

        if (self.pos[0] == self.destin[0] and self.pos[1] == self.destin[1]):
            best_position=self.pos
            
        self.pos = best_position
        self.distance=sum(abs(best_position - self.destin))
        self.trajectory.append(list(self.pos))
#-----------------------------------------------------

#Size of lattice; origin and destination; minimum distance between origin and destination; keep the trajectory with a list of nodes
#---------------------------------
N=6 #Length-width of grid
aerospace=grid(N,N) # Define object aerospace from class grid



n_planes=4

#Define objects plane from class plane
ori_plane0_0,dest_plane0_0 = [0,0], [5,5]
plane0=plane(ori_plane0_0, dest_plane0_0) #Define object with origin and destination
plane1=plane([5,5], [0,0]) #Define a second object (plane) with opposite destination/origin
plane2=plane([0,5], [5,0]) #Define object with origin and destination
plane3=plane([5,0], [0,5]) #Define a second object (plane) with opposite destination/origin
plane4=plane([0,0], [2,2])
planes=[plane0,plane1,plane2,plane3,plane4]


print("starting at:", plane0.origin, ". Destination:", plane0.destin, ". Minimum distance:", plane0.distance)
print("starting at:", plane1.origin, ". Destination:", plane1.destin, ". Minimum distance:", plane1.distance)
print("starting at:", plane2.origin, ". Destination:", plane2.destin, ". Minimum distance:", plane2.distance)
print("starting at:", plane3.origin, ". Destination:", plane3.destin, ". Minimum distance:", plane3.distance)

#Initialize the aerospace
aerospace.initialize_transit(planes)
print(aerospace.matrix)


for t in np.arange(10):
    
    plane0.update_pos_optimally(plane0.pos)
    plane1.update_pos_optimally(plane1.pos)
    plane2.update_pos_optimally(plane2.pos)
    plane3.update_pos_optimally(plane3.pos)
    plane4.update_pos_optimally(plane3.pos)

    aerospace.transit_state(planes)


    print(aerospace.matrix)
    
print(plane0.trajectory)
print(plane1.trajectory)
print(plane2.trajectory)
print(plane3.trajectory)


#Save trajectories to dataframe and dataframe to csv
#---------------------------------
x_move0=[step[0] for step in plane0.trajectory]
y_move0=[step[1] for step in plane0.trajectory]

x_move1=[step[0] for step in plane1.trajectory]
y_move1=[step[1] for step in plane1.trajectory]

d_tr = pd.DataFrame({'plane0_x' : x_move0, 'plane0_y': y_move0,'plane1_x' : x_move1, 'plane1_y': y_move1 })
d_tr.to_csv('../data/' + 'trajectories_classes_size_' + str(N) + '_planes_' + str(n_planes)+  '.csv')
#---------------------------------
