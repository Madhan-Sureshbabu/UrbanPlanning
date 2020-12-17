from hill_climbing import urban_plan

class GA(urban_plan) :
	
    def genetic_algorithm(self,terrain,max_I,max_C,max_R) : 
        start_time = time.time()
        population_size = 250

        elitism_size = int(0.25*population_size)
        culling_size = int(0.00*population_size)
        mutation_size = int(0.00*population_size)
        
        flag = 0
        num_attempts = 0
        temp_population = []
        population = []
        next_generation = []
        bestnow=[]
        bestnowtime=0
        gencount=0
        for i in range(population_size) : 
            terrain_map = np.copy(terrain)
            is_occupied, terrain_map = generate_random_starts(terrain_map, max_I, max_C, max_R,True)
            fitness_val = fitness_value(terrain,terrain_map,self.cost_map)
            heappush(next_generation, [fitness_val, terrain_map.tolist(), is_occupied.tolist()])

        # next generation contains initial candidates

        while (time.time() - start_time < 10) : 
            population = []
            population_fitness = []
            # copying current generation candidates to population array
            for i in range(population_size) :
                population.append(heappop(next_generation))
                population_fitness.append(population[i][0])
            
            gencount+=1

            if bestnow==[]:
                bestnow=population[population_size-1]
                bestnowtime=time.time() - start_time
            else:
                if bestnow[0]<population[population_size-1][0]:
                    bestnow=population[population_size-1]
                    bestnowtime=time.time() - start_time
            final_solution = population

            next_generation = []
            temp_population = []


            for i in range(culling_size) : 
                heappop(population)

            for j in reversed(range(len(population) - elitism_size, len(population))) : 
                heappush(next_generation,[population[j][0],population[j][1], population[j][2]])

            for i in range(mutation_size) : 
                index = np.random.randint(len(population))
                mutant = population[index]

                mutant_industrial_locations = []
                mutant_residential_locations = []
                mutant_commercial_locations = []

                industrial_locations_index = np.where(np.asarray(mutant[1])=='I')
                for i in range(len(industrial_locations_index[0])) : 
                    mutant_industrial_locations.append((industrial_locations_index[0][i],industrial_locations_index[1][i]))
                
                residential_locations_index = np.where(np.asarray(mutant[1])=='R')
                for i in range(len(residential_locations_index[0])) : 
                    mutant_residential_locations.append((residential_locations_index[0][i],residential_locations_index[1][i]))

                commercial_locations_index = np.where(np.asarray(mutant[1])=='C')
                for i in range(len(commercial_locations_index[0])) : 
                    mutant_commercial_locations.append((commercial_locations_index[0][i],commercial_locations_index[1][i]))

                # Swapping randomly any two zones (R-I, C-I, R-C)
                zone_prob = np.random.random_sample(1)
                if zone_prob < 0.3 : 
                    industrial_locations_index = np.random.randint(len(mutant_industrial_locations))
                    commercial_locations_index = np.random.randint(len(mutant_commercial_locations))
                    industry_position = mutant_industrial_locations[industrial_locations_index]
                    commercial_position = mutant_commercial_locations[commercial_locations_index]
                    population[index][1][industry_position[0]][industry_position[1]] = 'C'
                    population[index][1][commercial_position[0]][commercial_position[1]] = 'I'

                if zone_prob >= 0.3 and zone_prob < 0.6 :
                    industrial_locations_index = np.random.randint(len(mutant_industrial_locations))
                    residential_locations_index = np.random.randint(len(mutant_residential_locations))
                    industry_position = mutant_industrial_locations[industrial_locations_index]
                    residential_position = mutant_residential_locations[residential_locations_index]
                    population[index][1][industry_position[0]][industry_position[1]] = 'R'
                    population[index][1][residential_position[0]][residential_position[1]] = 'I'

                if zone_prob >= 0.6 :
                    commercial_locations_index = np.random.randint(len(mutant_commercial_locations))
                    residential_locations_index = np.random.randint(len(mutant_residential_locations))
                    commercial_position = mutant_commercial_locations[commercial_locations_index]
                    residential_position = mutant_residential_locations[residential_locations_index]
                    population[index][1][commercial_position[0]][commercial_position[1]] = 'R'
                    population[index][1][residential_position[0]][residential_position[1]] = 'C'
                
                population[index][0] = fitness_value(terrain,population[index][1],self.cost_map)

            heapify(population)
            
            while (len(next_generation)<population_size) : 

                curr_population_size = len(population)
                index = np.asarray(range(curr_population_size))
                probability = index / float(curr_population_size *(curr_population_size -1) / 2)

                index1 = np.random.choice(index,p=probability)
                index2 = np.random.choice(index,p=probability)
                while (index2 == index1) :
                    index2 = np.random.choice(index,p=probability)
                
                parent1 = population[index1]
                parent2 = population[index2]

                p1_industrial_locations = []
                p1_residential_locations = []
                p1_commercial_locations = []

                p2_industrial_locations = []
                p2_residential_locations = []
                p2_commercial_locations = []

                # finding out locations of Industries, Commercial and Residential locations of the two parents
                industrial_locations_index = np.where(np.asarray(parent1[1])=='I')
                for i in range(len(industrial_locations_index[0])) : 
                    p1_industrial_locations.append((industrial_locations_index[0][i],industrial_locations_index[1][i]))
                
                residential_locations_index = np.where(np.asarray(parent1[1])=='R')
                for i in range(len(residential_locations_index[0])) : 
                    p1_residential_locations.append((residential_locations_index[0][i],residential_locations_index[1][i]))

                commercial_locations_index = np.where(np.asarray(parent1[1])=='C')
                for i in range(len(commercial_locations_index[0])) : 
                    p1_commercial_locations.append((commercial_locations_index[0][i],commercial_locations_index[1][i]))

                industrial_locations_index = np.where(np.asarray(parent2[1])=='I')
                for i in range(len(industrial_locations_index[0])) : 
                    p2_industrial_locations.append((industrial_locations_index[0][i],industrial_locations_index[1][i]))
                
                residential_locations_index = np.where(np.asarray(parent2[1])=='R')
                for i in range(len(residential_locations_index[0])) : 
                    p2_residential_locations.append((residential_locations_index[0][i],residential_locations_index[1][i]))

                commercial_locations_index = np.where(np.asarray(parent2[1])=='C')
                for i in range(len(commercial_locations_index[0])) : 
                    p2_commercial_locations.append((commercial_locations_index[0][i],commercial_locations_index[1][i]))

                next_terrain_map = np.copy(terrain)
                
                is_occupied = np.zeros(terrain.shape)

                for i in range(len(terrain)) : 
                    for j in range(len(terrain[0])) : 
                        if next_terrain_map[i][j] == 'X' : 
                            is_occupied[i][j] = 1

        
                numI = np.random.randint(0,max_I+1)
                numC = np.random.randint(0,max_C+1)
                numR = np.random.randint(0,max_R+1)
                i = 0
                flag = 0
                while (i<min(numI,max(len(p1_industrial_locations), len(p2_industrial_locations)))) : 
                    parent_probability = np.random.random_sample(1)
                    if parent_probability >= 0.5 and len(p1_industrial_locations) > 0 :
                        index = np.random.randint(len(p1_industrial_locations))
                        if is_occupied[p1_industrial_locations[index][0]][p1_industrial_locations[index][1]] == 0 : 
                            is_occupied[p1_industrial_locations[index][0]][p1_industrial_locations[index][1]] = 1
                            next_terrain_map[p1_industrial_locations[index][0]][p1_industrial_locations[index][1]] = 'I'
                            i += 1
                    elif len(p2_industrial_locations) > 0  : 
                        index = np.random.randint(len(p2_industrial_locations))
                        if is_occupied[p2_industrial_locations[index][0]][p2_industrial_locations[index][1]] == 0 : 
                            is_occupied[p2_industrial_locations[index][0]][p2_industrial_locations[index][1]] = 1
                            next_terrain_map[p2_industrial_locations[index][0]][p2_industrial_locations[index][1]] = 'I'
                            i += 1  
                i = 0
                while (i<min(numC, max(len(p1_commercial_locations),len(p2_commercial_locations)))) :
                    parent_probability = np.random.random_sample(1)
                    if parent_probability >= 0.5 and len(p1_commercial_locations) > 0 :
                        index = np.random.randint(len(p1_commercial_locations))
                        if is_occupied[p1_commercial_locations[index][0]][p1_commercial_locations[index][1]] == 0 : 
                            is_occupied[p1_commercial_locations[index][0]][p1_commercial_locations[index][1]] = 1
                            next_terrain_map[p1_commercial_locations[index][0]][p1_commercial_locations[index][1]] = 'C'
                            i += 1
                    elif len(p2_commercial_locations) > 0  : 
                        index = np.random.randint(len(p2_commercial_locations))
                        if is_occupied[p2_commercial_locations[index][0]][p2_commercial_locations[index][1]] == 0 : 
                            is_occupied[p2_commercial_locations[index][0]][p2_commercial_locations[index][1]] = 1
                            next_terrain_map[p2_commercial_locations[index][0]][p2_commercial_locations[index][1]] = 'C'
                            i += 1
                    num_attempts += 1
                    if num_attempts > 10 * numC : 
                        flag = 1
                        break
                i = 0
                num_attempts = 0
                if flag == 0 : 
                    while (i<min(numR, max(len(p1_residential_locations),len(p2_residential_locations)))) :
                        parent_probability = np.random.random_sample(1)
                        if parent_probability >= 0.5 and len(p1_residential_locations) > 0:
                            index = np.random.randint(len(p1_residential_locations))
                            if is_occupied[p1_residential_locations[index][0]][p1_residential_locations[index][1]] == 0 : 
                                is_occupied[p1_residential_locations[index][0]][p1_residential_locations[index][1]] = 1
                                next_terrain_map[p1_residential_locations[index][0]][p1_residential_locations[index][1]] = 'R'
                                i += 1
                        elif len(p2_residential_locations) > 0  : 
                            index = np.random.randint(len(p2_residential_locations))
                            if is_occupied[p2_residential_locations[index][0]][p2_residential_locations[index][1]] == 0 : 
                                is_occupied[p2_residential_locations[index][0]][p2_residential_locations[index][1]] = 1
                                next_terrain_map[p2_residential_locations[index][0]][p2_residential_locations[index][1]] = 'R'
                                i += 1
                        num_attempts += 1
                        if num_attempts > 10 * numR : 
                            flag = 1
                            break
                num_attempts = 0
                if flag == 0  :
                    new_fitness_val = fitness_value(terrain,next_terrain_map,self.cost_map)
                    heappush(next_generation,[new_fitness_val,next_terrain_map.tolist(),is_occupied.tolist()])
            
        a = []
        for i in range(len(final_solution)):    a.append(heappop(final_solution))

        print("Printing the best solution found within the given time")
        print("\nScore:", bestnow[0])
        print("\nTime at which the best score was first obtained(secs):", round(bestnowtime,3))
        print("\nMap for the score:")
        b = np.array(bestnow[1])
        for i1 in range(b.shape[0]):
            for j1 in range(b.shape[1]):
                if b[i1][j1].isalpha() == False:
                    b[i1][j1] = ' '
        print(np.array(b))
        print("\nTotal number of generations:", gencount)
        print("------")
