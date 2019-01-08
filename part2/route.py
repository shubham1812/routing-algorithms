#!/bin/python
# route.py
# modified by araghuv-sgodshal-rojraman
####################################################################################################################
#Problem Statement: To implement algorithms that find good driving directions between pairs of cities given by the user.
#Given Inputs: start-city, end-city, routing-algorithm, cost-function
#Initial State S0: start-city
#State space S: Consist of all the valid states which can be traversed and has a path from start-city to end-city.
#Successor function S': A valid successor function to this problem gives the next city which can be visited to minimize the
#distance and gives good driving directions between the pair of cities given by user.
#Goal State: When successor of the current state is the end city.
#
#Abnormal Data: 1) When speed for a city is 0, The code changes the data into 1.
#               2) When a speed or highway distance is missing the program completely ignores  the line.
#               3) If city-gps.txt file does not have a city but road-segments.txt has it then the program omits the path to look for a new one. This might cause few paths to not be found.
#               4) We assume that all the data provided are accurate.
#
#Heuristic: 1) We are using a circular distance calculator to calculate the distance between two geological coordinates.
#        2) This also means that if the distance obtained from the circular distance is less than the highway distance then the path resultant path also might be wrong.
#        3) Astar with time as heuristic, the program finds the max-speed when loading the data and uses the same data for calculation.
#        4) Astar with segments as heuristic, the program finds the maximum highway length while loading the data and uses the same data for heuristic calculation.
#
#Observations:
#        1) Uniform cost search: This search algorithm always gives optimal result with segments as cost function.
#        2) Astar: Because of the above stated heuristic assumptions, this algorithm might not give optimal path as uniform cost search.
#        3) DFS: Not optimal
#        4) IDS: For most cases this algorithm gives the same solution as BFS as this data structure uses stack it might vary for a few test cases.
#        5) BFS: Assuming the segment cost is uniform, it is optimal.

#Input format: There should always be 4 parameters for the program to run
########################################################################################################################

import sys
from collections import defaultdict
from math import sin, cos, sqrt, atan2
from Queue import PriorityQueue
 
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items()
                            if len(locs)>1)

#successor function to find all the successors of the current city
def successor((path_so_far,city,h,t)):
    if city in visited:
        return [(0,0,0,0)]
    connected_cities = []
    index = dest_city.get(city)
    try:
        if index is None and city in to_city:
            connected_cities.append((path_so_far + " " + from_city[to_city.index(city)],from_city[to_city.index(city)],int(h)+int(highway_distance[to_city.index(city)]),float(t)+(float(highway_distance[to_city.index(city)])/float(speed_limit[to_city.index(city)])))) if from_city[to_city.index(city)] not in visited else 0
        elif index is not None:
            for i in index:
                connected_cities.append((path_so_far + " "  + from_city[i] , from_city[i],int(h) + int(highway_distance[i]), float(t) + (float(highway_distance[i])/float(speed_limit[i])))) if from_city[i] not in visited else 0

        start_index = from_city.index(city)
        for i in range(start_index,len(from_city)):
            if(from_city[i] != city):
                break
            connected_cities.append((path_so_far + " " + to_city[i] , to_city[i], int(h) + int(highway_distance[i]), float(t) + (float(highway_distance[i])/float(speed_limit[i])))) if to_city[i] not in visited else 0
    except:
        c = 2
    visited.append(city)
    if len(connected_cities) < 1:
        return [(0,0,0,0)]
    return connected_cities

#astar function with cost functions
def astar(start_city,end_city,cost_function):
    fringe = PriorityQueue()
    fringe.put((heuristic(start_city,end_city,cost_function),(start_city, start_city,"0","0")))
    while not fringe.empty() :
        (priority,(path_so_far, city,highway,time)) = fringe.get()
        for (path,succ_city,h,t) in successor((path_so_far,city,highway,time)):
            if succ_city!= 0:
                if end_city == succ_city :
                    return (path,h,t) 
                calculate_heuristic = heuristic(succ_city,end_city,cost_function)
                g = 0
                if cost_function == "distance":
                    g = h
                elif cost_function == "segments":
                    g = len(path.split(" "))+1
                else: 
                    g = t
                if calculate_heuristic != -1:
                    fringe.put((calculate_heuristic + g, (str(path),succ_city,h,t))) 
    return ((False,False,False))

#function to find heuristic value based on cost function
def heuristic(successor,end_city,cost_function):
    heuristic_value =  0
    if cost_function == "distance":
        heuristic_value = get_distance(successor,end_city)
    if cost_function == "time":
        heuristic_value = get_distance(successor,end_city)/float(max_speed)
    if cost_function == "segments":
        heuristic_value = get_distance(successor,end_city)/float(max_length)
    return heuristic_value

# function to calculate circular distance between two point
#https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def get_distance(succ_city,end_city):
    try:
        succ_lat = float(latitude[city_names.index(succ_city)])
        succ_long = float(longtitude[city_names.index(succ_city)])
        end_lat = float(latitude[city_names.index(end_city)])
        end_long = float(longtitude[city_names.index(end_city)])
        dlon = float(end_long) - float(succ_long)
        dlat = float(end_lat) - float(succ_lat)
        a = float(sin(dlat / 2)**2 + cos(succ_lat) * cos(end_lat) * sin(dlon / 2)**2)
        c = float(2 * atan2(sqrt(a), sqrt(1 - a)))
        distance = 6373.0 * c
        return distance
    except:
        return -1

#funtion for BFS
def Bfs(start,end) :
    fringe = [(start,start,"0","0")]
    while len(fringe) > 0 :
        for (path,s,h,t) in successor(fringe.pop(0)):
            if s!= 0:
                if s == end :
                    return (path,h,t)
                fringe.append((path,s,h,t))
    return ((False,False,False))

#function for DFS
def Dfs(start,end) :
    fringe = [(start,start,"0","0")]
    while len(fringe) > 0 :
        for (path,s,h,t) in successor(fringe.pop()):
            if s!= 0:
                if s == end :
                    return (path,h,t)
                fringe.append((path,s,h,t))
    return ((False,False,False))

#function for uniform cost search
def uniform(start_city,end_city,cost_function):
    fringe = PriorityQueue()
    fringe.put((0,(start_city, start_city,"0","0")))
    while not fringe.empty() :
        (priority,(path_so_far, city,highway,time)) = fringe.get()
        for (path,succ_city,h,t) in successor((path_so_far,city,highway,time)):
            if succ_city!= 0:
                if end_city == succ_city :
                    return (path,h,t) 
                g = 0
                if cost_function == "distance":
                    g = h
                elif cost_function == "segments":
                    g = len(path.split(" "))+1
                else: 
                    g = t
                fringe.put((g, (str(path),succ_city,h,t))) 
    return ((False,False,False))

#function for iterative deepening search
def Ids(start,end) :
    threshVal = 0
    threshold = 0
    fringe = [(start,start,"0","0")]
    while threshold < 50000:
        fringe = [(start,start,"0","0")]
        while len(fringe) > 0 :
            for (path,s,h,t) in successor(fringe.pop()):
                threshVal = threshVal + 1
                if s!= 0:
                    if s == end :
                        return (h,t,path)
                    if threshVal < threshold:
                        fringe.append((path,s,h,t))
            threshVal = threshVal + 1
        threshold +=1
        threshVal = 0
        del visited[:]
    return ((False,False,False))


visited  = []
start_state = []
start_city = sys.argv[1]
end_city = sys.argv[2]
routing_algorithm = sys.argv[3]
cost_function = sys.argv[4]
from_city = [] 
to_city = []
highway_distance = []
speed_limit = []
highway_name = []
dest_city = {}
city_names = []
latitude = []
longtitude = []
max_speed = 0
max_length = 0
#reading road-segments file
with open("road-segments.txt", 'r') as file:
    for line in file:
        divide = line.split(" ")
        if len(divide) > 4:
            from_city.append(divide[0])
            to_city.append(divide[1])
            highway_distance.append(divide[2])
            speed_limit.append(divide[3]) if divide[3] != "0" else speed_limit.append("1")
            highway_name.append(divide[4])
            if max_length < divide[2] :
                max_length = divide[2]
            if max_speed < divide [3]:
                max_speed = divide[3]
for dup,count in sorted(list_duplicates(to_city)):
    dest_city[dup] = count

#reading city gps values files
with open("city-gps.txt", 'r') as file:
    for line in file:
        divide = line.split(' ')
        city_names.append(divide[0])
        latitude.append(divide[1])
        longtitude.append(divide[2])

#print from_city[to_city.index('Bloomington,_Indiana')]

optimal = "no"
if routing_algorithm == 'bfs':
    (path,h,t) = Bfs(start_city,end_city)
    optimal = "yes"
if routing_algorithm == 'dfs':
    (path,h,t) = Dfs(start_city,end_city)   
    optimal = "no"
if routing_algorithm == 'astar':
    (path,h,t) = astar(start_city,end_city,cost_function) 
    optimal = "no"
if routing_algorithm == 'uniform':
    (path,h,t) = uniform(start_city,end_city,cost_function) 
    if cost_function == 'segments':
        optimal = "yes"
if routing_algorithm == 'ids':
    (h,t,path) = Ids(start_city,end_city) 
    optimal = "yes"

if not path:
    print "No path exists"
else :
    print optimal + " " +str(h)+" "+str(t)+" "+path
