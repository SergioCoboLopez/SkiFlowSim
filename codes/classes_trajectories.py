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
        self.width=N
        self.length=M

    #Initialize the matrix with the origins of all planes in the grid
    def initialize_transit(self, planes):
        for p in planes:
            self.matrix[p.origin[0], p.origin[1]]+=1
            
    #Update positions of one plane in grid 
    def one_plane_transit_state(self,plane):
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
        self.priority=rnd.randint(1,10)

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
    def update_pos_optimally(self, pos, airspace, max_planes):

        capability = 2 
        movements = [np.array([0,-1]), np.array([-1,0]), np.array([0,1]), np.array([1,0])] 

        possible_positions = [self.pos + movement for movement in movements]
        possible_positions = [pos for pos in possible_positions if (pos[0] < airspace.width and pos[0] >= 0) and (pos[1] < airspace.length and pos[1] >= 0)] #Avoid to be out of frontiers

        #If final destination is an airport, it has maximum capability
        for pos in possible_positions:
            if (self.destin[0] == pos[0]) and (self.destin[1] == pos[1]):
                capability = max_planes
                break
            
        possible_positions = [pos for pos in possible_positions if airspace.matrix[pos[0]][pos[1]] < capability] 
        possible_distances=[sum(abs(possible_position - self.destin)) for possible_position in possible_positions]
        
        min_distance=possible_distances.index(min(possible_distances))
        best_position=possible_positions[min_distance]

        if (self.pos[0] == self.destin[0] and self.pos[1] == self.destin[1]):
            best_position=self.pos
            
        self.pos = best_position
        self.distance=sum(abs(best_position - self.destin))
        self.trajectory.append(list(self.pos))

        airspace.one_plane_transit_state(self)
#-----------------------------------------------------

#Size of lattice; origin and destination; minimum distance between origin and destination; keep the trajectory with a list of nodes
#---------------------------------
N,M=6,6 #Length-width of grid
airspace=grid(N,M) # Define object airspace from class grid



n_planes=6

#Encompass possible origins and destinations (nomes diagonals de moment)
possible_origins = [[0,0],[N-1,N-1]]
possible_destinations = [[0,0],[N-1,N-1]]

#Define objects plane from class plane
planes = []
for i in range(n_planes):
    origin = rnd.choice(possible_origins)
    destination = rnd.choice(possible_destinations)
    while origin == destination:
        destination = rnd.choice(possible_destinations)
    planes.append(plane(origin, destination))

for p in planes:
    print("starting at:", p.origin, ". Destination:", p.destin, ". Minimum distance:", p.distance)

#Initialize the airspace
airspace.initialize_transit(planes)
print(airspace.matrix)


for t in np.arange(10):

    for p in planes:
        print(p,p.priority)
    
    #Priority order
    planes_order = sorted(planes, key=lambda plane: plane.priority, reverse=True)

    for p in planes:
        p.update_pos_optimally(p.pos,airspace,n_planes)

    '''planes_conflictius = airspace.check_capability(planes) #retornar planes_conflictius
    for p in planes_conflictius:
         p.update_pos_optimally(p.pos,airspace) #S'ha d'incloure que no torni a fer el moviment prohibit'''
    
    print(airspace.matrix)

print("Trajectories")
for p in planes:
    print(p.trajectory)


quit()
#Save trajectories to dataframe and dataframe to csv 
#---------------------------------
#Falta fer aixo de forma generica per n_planes
x_move0=[step[0] for step in plane0.trajectory]
y_move0=[step[1] for step in plane0.trajectory]

x_move1=[step[0] for step in plane1.trajectory]
y_move1=[step[1] for step in plane1.trajectory]

d_tr = pd.DataFrame({'plane0_x' : x_move0, 'plane0_y': y_move0,'plane1_x' : x_move1, 'plane1_y': y_move1 })
d_tr.to_csv('../data/' + 'trajectories_classes_size_' + str(N) + '_planes_' + str(n_planes)+  '.csv')
#---------------------------------
