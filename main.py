import numpy as np
import time
from heapq import heappush, heappop, heapify
import sys
from os import path
from urbanplan_utils import *
from hill_climbing import HC
from genetic_algorithm import GA

if __name__=="__main__" : 
    filename=sys.argv[1]
    print (filename)
    if path.exists(filename)==False:
        print ("Incorrect filename")
        sys.exit()

    algo=sys.argv[2]
    f = open(filename, 'r')
    lines = f.readlines()
    terrain = []
    buildings = []
    nlines = 0
    for line in lines:
        line = line.rstrip()
        if nlines < 3:
            buildings.append((line))
        else:
            terrain.append([item for item in line.split(',')])
        nlines += 1

    b_i = int(buildings[0])
    b_c = int(buildings[1])
    b_r = int(buildings[2])
    terrain =np.array(terrain)
    for i in range(len(terrain)):
        for j in range(len(terrain[0])):
            if terrain[i][j]!='X' and terrain[i][j]!='S':
                terrain[i][j]=int(terrain[i][j])

    print("Max. Industrial zones\t:",b_i)
    print("Max. Commercial zones\t:",b_c)
    print("Max. Residential zones\t:",b_r)
    print("Input map with cost:")
    print(terrain)
    
    print("-----")

    # U = urban_plan(terrain)
    if algo=='HC':
    	U = HC(terrain)
    	U.hill_climbing(terrain,b_i,b_c,b_r)
    elif algo=='GA':  
    	U = GA(terrain)   
    	U.genetic_algorithm(terrain,b_i,b_c,b_r)
    else:
        print ("Invalid Algo method")
