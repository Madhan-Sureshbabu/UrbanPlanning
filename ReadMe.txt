## Urban Planning using Hill Climbing and Genetic Algorithm

### Problem Statement

#### Input map contains the following symbols  :

1. X: former toxic waste site. Industrial zones within 2 tiles take a penalty of -10.
Commercial and residential zones within 2 tiles take a penalty of -20. You cannot build
directly on a toxic waste site.

2. S: scenic view. Residential zones within 2 tiles gain a bonus of 10 points. If you wish,
you can build on a scenic site but it destroys the view. Building on a scenic view has a
cost of 1.

3. 1...9: how difficult it is to build on that square. To build a zone on any square costs
2+difficulty. So building a Commercial zone on a square of difficulty 6 costs 8 points.
You will receive a penalty of that many points to put any zone on that square.

#### Industrial, Residential, and Commercial tiles are required to be built on the terrain optimally based on the following constraints : 

1. Industrial tiles benefit from being near other industry. For each industrial tile within 2
squares, there is a bonus of 2 points.

2. Commercial sites benefit from being near residential tiles. For each residential tile within
3 squares, there is a bonus of 4 points. However, commercial sites do not like
competition. For each commercial site with 2 squares, there is a penalty of 4 points.

3.Residential sites do not like being near industrial sites. For each industrial site within 3
squares there is a penalty of 5 points. However, for each commercial site with 3 squares
there is a bonus of 4 points.

< Manhatatan distance is used for all distance measurements >

#### Example Input : 

[['2' '3' '3' 'X' '6']
 ['4' 'X' '3' '2' '3']
 ['3' '1' '1' '6' 'X']
 ['7' '6' '5' '8' '5']
 ['S' '6' 'S' '9' '1']
 ['4' '7' '2' '6' '5']]

#### Output : 

[[' ' ' ' ' ' 'X' ' ']
 [' ' 'X' ' ' ' ' ' ']
 [' ' ' ' ' ' ' ' 'X']
 [' ' ' ' ' ' ' ' ' ']
 ['S' 'R' 'S' ' ' ' ']
 [' ' 'R' 'C' ' ' 'I']]

### Usage 
Arguments : [map.txt] [Algo]
map.txt	  :	name of the txt file with the map and number of zones in the same format at the sample imput given
Algo 	  :	HC for hillclimbing, GA for genetic Algo

Example command line input:
-------------------------
python3 main.py map2.txt HC

This runs the code for the map in map2.txt using the HillClimbing algorithm

-------------------------
python3 main.py map1.txt GA

This runs the code for the map in map1.txt using the Genetic Algorithm


