import numpy as np
import time
from heapq import heappush, heappop, heapify
import sys
from os import path

def generate_index(is_occupied) : 
    while(True) : 
        index_0 = np.random.randint(len(is_occupied))
        index_1 = np.random.randint(len(is_occupied[0]))
        if (is_occupied[index_0][index_1]==0) : 
            break
    is_occupied[index_0][index_1] = 1
    return index_0,index_1

def calc_manhattan_distance(pt1,pt2) : 
    return np.absolute(pt1[0] - pt2[0]) + np.absolute(pt1[1] - pt2[1])

def update_occupied(terrain_map,is_occupied) : 
    is_occupied = np.zeros(is_occupied.shape)
    for i in range(len(terrain_map)) : 
        for j in range(len(terrain_map[0])) : 
            if terrain[i][j] == 'X' or terrain[i][j] == 'S' or terrain_map[i][j] == 'I' or terrain_map[i][j] == 'R' or terrain_map[i][j] == 'C'  :
                is_occupied[i][j] = 1
    return is_occupied

def calc_cost(terrain,terrain_map,cost_map) : 
    cost = 0
    residential_locations = []
    commercial_locations = []
    industrial_locations = []
    waste_locations = []
    scenic_view = []

    waste = np.where(terrain=='X')
    for i in range(len(waste[0])) : 
        waste_locations.append((waste[0][i],waste[1][i]))

    residential = np.where(terrain_map=='R')
    for i in range(len(residential[0])) : 
        residential_locations.append((residential[0][i],residential[1][i]))

    industrial = np.where(terrain_map=='I')
    for i in range(len(industrial[0])): 
        industrial_locations.append((industrial[0][i],industrial[1][i]))

    commercial = np.where(terrain_map=='C')
    for i in range(len(commercial[0])) : 
        commercial_locations.append((commercial[0][i],commercial[1][i]))

    scenic = np.where(terrain_map=='S')
    
    for i in range(len(scenic[0])) : 
        scenic_view.append((scenic[0][i],scenic[1][i]))

    for waste_location in waste_locations : 
        for industrial_location in industrial_locations : 
            if calc_manhattan_distance(waste_location,industrial_location) <= 2 : 
                cost += 10
        for commercial_location in commercial_locations : 
            if calc_manhattan_distance(waste_location,commercial_location) <= 2 : 
                cost += 20
        for residential_location in residential_locations : 
            if calc_manhattan_distance(waste_location,residential_location) <= 2 : 
                cost += 20

    for view in scenic_view : 
        for residential_location in residential_locations : 
            if calc_manhattan_distance(view,residential_location) <= 2 and calc_manhattan_distance(view,residential_location) > 0 : 
                cost -= 10

    for residential_location in residential_locations : 
        cost += cost_map[residential_location[0]][residential_location[1]] + 2
        for industrial_location in industrial_locations :  
            if calc_manhattan_distance(residential_location,industrial_location) <= 3 :
                cost += 5

        for commercial_location in commercial_locations : 
            if calc_manhattan_distance(residential_location,commercial_location) <= 3 : 
                cost -= 4

    for i in range(len(industrial_locations)) : 
        industrial_location = industrial_locations[i]
        cost += cost_map[industrial_location[0]][industrial_location[1]] + 2 
        for j in range(i+1,len(industrial_locations)) : 
            industrial_location2 = industrial_locations[j]  
            dist = calc_manhattan_distance(industrial_location, industrial_location2)
            if dist > 0 and dist <= 2 : 
                cost -= 2
                
    for i in range(len(commercial_locations)) : 
        commercial_location = commercial_locations[i]
        cost += cost_map[commercial_location[0]][commercial_location[1]] + 2
        for j in range(i+1,len(commercial_locations)) :
            commercial_location2 = commercial_locations[j]
            dist = calc_manhattan_distance(commercial_location,commercial_location2)
            if dist > 0 and dist <= 2 : 
                cost += 4
    return cost

def fitness_value(terrain,map1,cost_map) : 
    # print map1
    return -1 * calc_cost(terrain,map1,cost_map)

def update_T(T) : 
    return T*0.9
    # return 10 - np.log(T)

def annealing_probability(fit, new_fit, T) :
    if new_fit >= fit : 
        return 1
    else : 
        return np.exp((new_fit - fit)/T)

def generate_random_starts(terrain_map, max_I, max_C, max_R, GA):
    cand_map = np.copy(terrain_map)
    is_occupied = np.zeros(terrain_map.shape)
    
    for i in range(len(terrain_map)) : 
        for j in range(len(terrain_map[0])):
            if terrain_map[i][j] == 'X' : 
                is_occupied[i][j] = 1

    if GA == False : 
        num_I = int(max_I / 2) 
        num_R = int(max_R / 2)
        num_C = int(max_C / 2)
        if num_I == 0 : 
            num_I = 1
        if num_C == 0 : 
            num_C = 1
        if num_R == 0 : 
            num_R = 1

    else : 				# For GA generate initial maps with max number of 'I' 'C' & 'R'
        num_R = max_R
        num_I = max_I
        num_C = max_C

    for i in range(num_I) :
        industrial_index_0,industrial_index_1 = generate_index(is_occupied)
        cand_map[industrial_index_0][industrial_index_1] = 'I'

    for i in range(num_C) : 
        commercial_index_0,commercial_index_1 = generate_index(is_occupied)
        cand_map[commercial_index_0][commercial_index_1] = 'C'
    
    for i in range(num_R) : 
        residential_index_0, residential_index_1 = generate_index(is_occupied)
        cand_map[residential_index_0][residential_index_1] = 'R'

    return is_occupied, cand_map
