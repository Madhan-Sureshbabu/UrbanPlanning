import numpy as np
import time
from heapq import heappush, heappop, heapify
import sys
from os import path
from urbanplan_utils import *

class urban_plan : 
    def __init__(self,terrain) : 
        self.side_ways = 0
        self.possible_solutions = []
        self.fitind=[]
        self.nrestarts=0
        self.cost_map = np.zeros(terrain.shape)
        self.terrain = terrain
        for i in range(len(self.terrain)) : 
            for j in range(len(self.terrain[0])) : 
                if self.terrain[i][j] == 'S' : 
                    self.cost_map[i][j] = -1
                elif self.terrain[i][j] != 'X' :
                    self.cost_map[i][j] = int(terrain[i][j])

    def get_cost_map(self) :
        return self.cost_map

class HC(urban_plan) :

    def move(self,terrain_map,is_occupied, max_I, max_C, max_R, T, stime):
        empty_map_flag = 0
        fitness_val = fitness_value(self.terrain,terrain_map,self.cost_map)
        industrial_locations = []
        residential_locations = []
        commercial_locations = []

        industrial_locations_index = np.where(terrain_map=='I')
        for i in range(len(industrial_locations_index[0])) : 
            industrial_locations.append((industrial_locations_index[0][i],industrial_locations_index[1][i]))
        
        residential_locations_index = np.where(terrain_map=='R')
        for i in range(len(residential_locations_index[0])) : 
            residential_locations.append((residential_locations_index[0][i],residential_locations_index[1][i]))

        commercial_locations_index = np.where(terrain_map=='C')
        for i in range(len(commercial_locations_index[0])) : 
            commercial_locations.append((commercial_locations_index[0][i],commercial_locations_index[1][i]))

        
        if len(industrial_locations) > 0 :
            # A random index from all the unoccupied positions are chosen
            next_industrial_0,next_industrial_1 = generate_index(is_occupied)
            next_terrain_map = np.copy(terrain_map)
            # An industry is set up there
            next_terrain_map[next_industrial_0][next_industrial_1] = 'I'
            
            # A current industry location is taken down
            swaping_industry_index = np.random.randint(len(industrial_locations))

            # Updating the new map by removing an existing Industrial location
            # terrain is the original un-planned map that has only 'X' 'S' and costs in all other locations
            # next_terrain_map has a new industry location and 1 old industry location is updated with its build cost
            next_terrain_map[industrial_locations[swaping_industry_index][0]][industrial_locations[swaping_industry_index][1]] \
            		= self.terrain[industrial_locations[swaping_industry_index][0]][industrial_locations[swaping_industry_index][1]]	
            
            # If this new configuration is better, it is kept. Otherwise the new map is not used.
            new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)
            if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val, T) :
                is_occupied[industrial_locations[swaping_industry_index][0]][industrial_locations[swaping_industry_index][1]] = 0
                terrain_map = np.copy(next_terrain_map)
                fitness_val = new_fitness_val
            else : 
                is_occupied[next_industrial_0][next_industrial_1] = 0

        else : 
            empty_map_flag += 1

        # Same applicable for Residential and Commercial locations
        if len(residential_locations) > 0 : 
            next_residential_0, next_residential_1 = generate_index(is_occupied)
            next_terrain_map = np.copy(terrain_map)
            next_terrain_map[next_residential_0][next_residential_1] = 'R'
            
            swapping_resident_index = np.random.randint(len(residential_locations))
            next_terrain_map[residential_locations[swapping_resident_index][0]][residential_locations[swapping_resident_index][1]] = self.terrain[residential_locations[swapping_resident_index][0]][residential_locations[swapping_resident_index][1]]
            new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)
            
            if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val, T) :
                is_occupied[residential_locations[swapping_resident_index][0]][residential_locations[swapping_resident_index][1]] = 0
                terrain_map = np.copy(next_terrain_map)
                fitness_val = new_fitness_val
            else : 
                is_occupied[next_residential_0][next_residential_1] = 0

        else : 
            empty_map_flag += 1
        
        if len(commercial_locations) > 0 :
            next_commercial_0, next_commercial_1 = generate_index(is_occupied)
            next_terrain_map = np.copy(terrain_map)
            next_terrain_map[next_commercial_0][next_commercial_1] = 'C'
            swapping_commercial_index = np.random.randint(len(commercial_locations))
            
            next_terrain_map[commercial_locations[swapping_commercial_index][0]][commercial_locations[swapping_commercial_index][1]] = self.terrain[commercial_locations[swapping_commercial_index][0]][commercial_locations[swapping_commercial_index][1]]
            new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)
             
            if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val,T) : 
                is_occupied[commercial_locations[swapping_commercial_index][0]][commercial_locations[swapping_commercial_index][1]] = 0
                terrain_map = np.copy(next_terrain_map)
                fitness_val = new_fitness_val
            else : 
                is_occupied[next_commercial_0][next_commercial_1] = 0

        else : 
            empty_map_flag += 1

        if empty_map_flag == 3 : 
            new_fitness_val = -10

        # If probability of keeping a change is lower than 0.0001, count as sideways moves
        if annealing_probability(fitness_val, new_fitness_val, T) < 0.0001 : 
            self.side_ways += 1

        # Restart if > 10
        if self.side_ways > 10 : 
            self.side_ways = 0
            T = 1000000
            self.nrestarts+=1
            heappush(self.possible_solutions,(-fitness_val,terrain_map.tolist(),time.time() - stime))
            self.fitind.append([fitness_val])
            terrain_map = np.copy(self.terrain)
            is_occupied, terrain_map = generate_random_starts(terrain_map, max_I, max_C, max_R,False)

        return terrain_map, is_occupied, T


    def add(self,terrain_map,is_occupied, max_I, max_R, max_C, T) : 
        fitness_val = fitness_value(self.terrain,terrain_map,self.cost_map)
        industrial_locations = []
        residential_locations = []
        commercial_locations = []

        industrial_locations_index = np.where(terrain_map=='I')
        for i in range(len(industrial_locations_index[0])) : 
            industrial_locations.append((industrial_locations_index[0][i],industrial_locations_index[1][i]))
        
        residential_locations_index = np.where(terrain_map=='R')
        for i in range(len(residential_locations_index[0])) : 
            residential_locations.append((residential_locations_index[0][i],residential_locations_index[1][i]))

        commercial_locations_index = np.where(terrain_map=='C')
        for i in range(len(commercial_locations_index[0])) : 
            commercial_locations.append((commercial_locations_index[0][i],commercial_locations_index[1][i]))

        num_I = len(industrial_locations)
        num_C = len(commercial_locations)
        num_R = len(residential_locations)

        zone_prob = np.random.random_sample(1)
        # zone_prob decides which zone among I R and C to add in the map
        if zone_prob < 1./3 : 
            if num_I < max_I : 
            	# Same logic as seen in move() function
                next_industrial_index_0,next_industrial_index_1 = generate_index(is_occupied)
                next_terrain_map = np.copy(terrain_map)
                next_terrain_map[next_industrial_index_0][next_industrial_index_1] = 'I'
        
                new_fitness_val = fitness_value(self.terrain, next_terrain_map,self.cost_map)

                if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val, T) :
                    terrain_map = np.copy(next_terrain_map)
                    fitness_val = new_fitness_val
                else : 
                    is_occupied[next_industrial_index_0][next_industrial_index_1] = 0

        if zone_prob >= 1./3 and zone_prob < 2./3 : 
            if num_C < max_C : 
                next_commercial_index_0, next_commercial_index_1 = generate_index(is_occupied)
                next_terrain_map = np.copy(terrain_map)
                next_terrain_map[next_commercial_index_0][next_commercial_index_1] = 'C'
        
                new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)

                if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val, T) :
                    terrain_map = np.copy(next_terrain_map)
                    fitness_val = new_fitness_val
                else : 
                    is_occupied[next_commercial_index_0][next_commercial_index_1] = 0

        if zone_prob >= 2./3 :
            if num_R < max_R : 
                next_residential_0, next_residential_1 = generate_index(is_occupied)
                next_terrain_map = np.copy(terrain_map)
                next_terrain_map[next_residential_0][next_residential_1] = 'R'

                new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)

                if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val, T) :
                    terrain_map = np.copy(next_terrain_map)
                    fitness_val = new_fitness_val
                else : 
                    is_occupied[next_residential_0][next_residential_1] = 0

        return terrain_map, is_occupied


    def remove(self,terrain_map,is_occupied, max_I, max_R, max_C, T) : 
        fitness_val = fitness_value(self.terrain,terrain_map,self.cost_map)
        industrial_locations = []
        residential_locations = []
        commercial_locations = []

        industrial_locations_index = np.where(terrain_map=='I')
        for i in range(len(industrial_locations_index[0])) : 
            industrial_locations.append((industrial_locations_index[0][i],industrial_locations_index[1][i]))
        
        residential_locations_index = np.where(terrain_map=='R')
        for i in range(len(residential_locations_index[0])) : 
            residential_locations.append((residential_locations_index[0][i],residential_locations_index[1][i]))

        commercial_locations_index = np.where(terrain_map=='C')
        for i in range(len(commercial_locations_index[0])) : 
            commercial_locations.append((commercial_locations_index[0][i],commercial_locations_index[1][i]))

        num_I = len(industrial_locations)
        num_C = len(commercial_locations)
        num_R = len(residential_locations)

        # Choose from which zone to remove a building
        zone_prob = np.random.random_sample(1)
        if zone_prob < 1./3 : 
            if num_I > 0 : 
                swapping_industry_index = np.random.randint(len(industrial_locations))

                next_terrain_map = np.copy(terrain_map)
                next_terrain_map[industrial_locations[swapping_industry_index][0]][industrial_locations[swapping_industry_index][1]] = self.terrain[industrial_locations[swapping_industry_index][0]][industrial_locations[swapping_industry_index][1]]

                new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)

                if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val, T) :
                    terrain_map = np.copy(next_terrain_map)
                    fitness_val = new_fitness_val
                    is_occupied[industrial_locations[swapping_industry_index][0]][industrial_locations[swapping_industry_index][1]] = 0           

        if zone_prob >= 1./3 and zone_prob < 2./3 : 
            if num_C > 0: 
                swapping_commercial_index = np.random.randint(len(commercial_locations))

                next_terrain_map = np.copy(terrain_map)
                next_terrain_map[commercial_locations[swapping_commercial_index][0]][commercial_locations[swapping_commercial_index][1]] = self.terrain[commercial_locations[swapping_commercial_index][0]][commercial_locations[swapping_commercial_index][1]]
                new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)
        
                if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val,T) : 
                    is_occupied[commercial_locations[swapping_commercial_index][0]][commercial_locations[swapping_commercial_index][1]] = 0
                    terrain_map = np.copy(next_terrain_map)
                    fitness_val = new_fitness_val
                
        if zone_prob >= 2./3 :
            if num_R > 0 : 
                swapping_resident_index = np.random.randint(len(residential_locations))
        
                next_terrain_map = np.copy(terrain_map)
                next_terrain_map[residential_locations[swapping_resident_index][0]][residential_locations[swapping_resident_index][1]] = self.terrain[residential_locations[swapping_resident_index][0]][residential_locations[swapping_resident_index][1]]
                new_fitness_val = fitness_value(self.terrain,next_terrain_map,self.cost_map)
        
                if np.random.random_sample(1) <= annealing_probability(fitness_val, new_fitness_val,T) : 
                    is_occupied[residential_locations[swapping_resident_index][0]][residential_locations[swapping_resident_index][1]] = 0
                    terrain_map = np.copy(next_terrain_map)
                    fitness_val = new_fitness_val

                
        return terrain_map, is_occupied


    def hill_climbing(self,terrain,max_I,max_R,max_C):	# terrain is the map input with cost values, 'X' and 'S'
        start_time = time.time()

        terrain_map = np.copy(terrain) 
        self.terrain = terrain
        self.side_ways = 0
        self.possible_solutions = []

        is_occupied, terrain_map = generate_random_starts(terrain_map, max_I, max_C, max_R,False)
        fitness_val = fitness_value(self.terrain, terrain_map,self.cost_map)
        print ("Initial configuration")
        print ("Score:", fitness_val)
        b1 = np.array(terrain_map)
        for i1 in range(b1.shape[0]):
            for j1 in range(b1.shape[1]):
                if b1[i1][j1].isalpha() == False:
                    b1[i1][j1] = ' '
        # print(b1)

        T = 1000000

        
        while (time.time() - start_time < 10) : 

            move_add_remove_prob = np.random.random_sample(1)

            if move_add_remove_prob <= 0.5 : 
                terrain_map, is_occupied, T = self.move(terrain_map,is_occupied,max_I, max_R, max_C,T, start_time)

            if move_add_remove_prob > 0.5 and move_add_remove_prob <= 0.6 : 
                terrain_map, is_occupied = self.add(terrain_map,is_occupied, max_I, max_R, max_C, T)

            if move_add_remove_prob > 0.6 and move_add_remove_prob <= 1 : 
                terrain_map, is_occupied = self.remove(terrain_map,is_occupied, max_I, max_R, max_C, T)

            T = update_T(T)
        
        if T < 10 : 
            fitness_val = fitness_value(self.terrain,terrain_map,self.cost_map)
            heappush(self.possible_solutions,(-fitness_val,terrain_map.tolist(),time.time() - start_time ))
            self.fitind.append([fitness_val])

        print ("------")

        [a,b,c]= heappop(self.possible_solutions)
        print("Printing the best solution found within the given time")
        print("\nScore:", -a)
        print("\nTime at which the best score was first obtained(secs):", round(c,3))
        print("\nMap for the score:")
        b = np.array(b)
        for i1 in range(b.shape[0]):
            for j1 in range(b.shape[1]):
                if b[i1][j1].isalpha() == False:
                    b[i1][j1] = ' '
        print(np.array(b))
        print("\nNumber of restarts:", self.nrestarts)
        print("------")

