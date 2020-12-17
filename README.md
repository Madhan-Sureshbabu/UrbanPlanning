## Urban Planning using Hill Climbing and Genetic Algorithm

### Problem Statement

To determine the ideal locations to build industrial, residential, and commerical zones in a city

### Dependencies
```
numpy
heapq
system
date_time
```

### Input map contains the following symbols  :

1. X: former toxic waste site. Industrial zones within 2 tiles take a penalty of -10.
Commercial and residential zones within 2 tiles take a penalty of -20. You cannot build
directly on a toxic waste site.

2. S: scenic view. Residential zones within 2 tiles gain a bonus of 10 points. If you wish,
you can build on a scenic site but it destroys the view. Building on a scenic view has a
cost of 1.

3. 1...9: how difficult it is to build on that square. To build a zone on any square costs
2+difficulty. So building a Commercial zone on a square of difficulty 6 costs 8 points.
You will receive a penalty of that many points to put any zone on that square.

#### Constraints

1. Industrial tiles benefit from being near other industry. For each industrial tile within 2
squares, there is a bonus of 2 points.

2. Commercial sites benefit from being near residential tiles. For each residential tile within
3 squares, there is a bonus of 4 points. However, commercial sites do not like
competition. For each commercial site with 2 squares, there is a penalty of 4 points.

3. Residential sites do not like being near industrial sites. For each industrial site within 3
squares there is a penalty of 5 points. However, for each commercial site with 3 squares
there is a bonus of 4 points.

Manhatatan distance is used for all distance measurements

#### Example Input : 

&nbsp; '2' &nbsp; '3' &nbsp; '3' &nbsp; 'X' &nbsp; '6'  
&nbsp; '4' &nbsp; 'X' &nbsp; '3' &nbsp; '2' &nbsp; '3'  
&nbsp; '3' &nbsp; '1' &nbsp; '1' &nbsp; '6' &nbsp; 'X'  
&nbsp; '7' &nbsp; '6' &nbsp; '5' &nbsp; '8' &nbsp; '5'  
&nbsp; 'S' &nbsp; '6' &nbsp; 'S' &nbsp; '9' &nbsp; '1'  
&nbsp; '4' &nbsp; '7' &nbsp; '2' &nbsp; '6' &nbsp; '5'  

#### Output : 
1 (Max num of Industrial zones)  
2 (Max num of Commercial zones)  
2 (Max num of Residential zones)  
&nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; 'X' &nbsp; ' &nbsp; '  
&nbsp; ' &nbsp; ' &nbsp; 'X' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; '  
&nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; 'X'  
&nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; '  
&nbsp; 'S' &nbsp; 'R' &nbsp; 'S' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; '  
&nbsp; ' &nbsp; ' &nbsp; 'R' &nbsp; 'C' &nbsp; ' &nbsp; ' &nbsp; ' &nbsp; '  

Score : 27

### Usage 
Arguments : [map.txt] [Algo]  
```bash
python3 main.py map2.txt HC  
```
This runs the code for the map in map2.txt using the HillClimbing algorithm

```bash
python3 main.py map1.txt GA  
```
This runs the code for the map in map1.txt using the Genetic Algorithm
