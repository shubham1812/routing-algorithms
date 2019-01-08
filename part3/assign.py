#!/bin/python
###############################################################################################
#                                                                                             
#The below implemented program uses Local Search - Monte Carlo(Partially).                    
#Tested with 100 student pref data.                                                           
#Cannot guarantee optimal result but on multiple runs it should come close to optimal result. 
#State Space: the state space has all the students in it with a maximum of 3 people in a group per state
# We first had to formulate the problem into a search problem for us to use local search. We fist used a BFS algorithm,
# the goal state was defined in such a way that atleast 70% of the students were satisfied and the
#cost of error rate was around 20% or less. But this was taking more time for large inputs.
#We then modified the goal state that only returns the total cost of the given state and then modified the 
#algorithm into a Monte-Carlo local search algorithm which gave us near optimal results when ran for more number of times.
# Initial Sate: It consists of all the students in different groups.
# Successor: This function will always join the first item with the remaining items in the state to generate all possible
# combinations. It also ensures that no state consists of a group size more than 3 and also avoids duplicates. To find an optimal 
# solution, we always need to go to the end of the depth of the node.
# Eg: Consider 3 students: [1][2][3] -> Initial State
#                          [[1,2][3]] [[1][2,3]] [[1,3][2]] -> 1st Level
#                          [[1,2,3]]                        -> 2nd Level
#Cost Function: This function will give a total cost of a state passed using K,M,N values.
###############################################################################################

import timeit
import random
import sys

#successor function: finding the successors with permutation to the current state
def successor(currentState):
    t = currentState[:]
    i = 0
    temp = []
    while i < len(currentState):
        key = currentState[i]
        t.pop(t.index(key))
        for k in range(len(t)):
            s = []
            m = 0
            te = key+t[k]
            if len(key) + len(t[k]) <=3 :
                s.append(te)
                m = len(key)+len(t[k])
                group.append(te)
            for j in range(len(currentState)):
                if t[k] != currentState[j] and key != currentState[j]:
                    s = s + [currentState[j]]
                    m = m + len(currentState[j])
            if m == total_count:
                temp.append(s)
        i += 1
    return temp

#returns cost of the state
def goal_state(state):
    total_cost = len(state)*k
    for i in state:
        group_size = len(i)
        for j in range(len(i)):
            t_list = i[:j]+i[j+1:]
            s = start_state.get(i[j]).split(" ")
            s[0] = group_size if int(s[0]) == 0 else s[0]
            if int(s[0]) != group_size:
                total_cost = total_cost + 1
            s1 = s[1].split(",")
            if len(set(t_list) & set(s1)) != len(s1) and s1.count('_') == 0:
                total_cost = total_cost + n
            s2 = s[2].split(",")
            if len(s2) > 0 and s2.count('_') == 0:
                dislike = len(set(t_list) & set(s2))
                total_cost = total_cost + m*dislike

    return total_cost


# partial monte carlo algorithm
def monte(state):
    min = 10000000
    iteration1 = 50
    int_state = state
    goal = goal_state(state)
    min_state = []
    if goal < min:
        min = goal
    while iteration1 > 0:
        state = int_state
        iteration = 1000
        while iteration > 0:
            state_space = successor(state)
            if len(state_space) > 0:
                s = state_space[random.randint(0,len(state_space)-1)]
            else:
                break
            current_cost = goal_state(s)
            state = s[:]
            if current_cost < min:
                min = current_cost
                min_state = s[:]
            iteration -= 1
        iteration1 -= 1
    for i in min_state:
        s = " ".join(i)
        print(s)
    print(min)


group = []

start_state = {}
total_count = 0
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])
start = timeit.default_timer()
#reading data from the input file
with open(sys.argv[1], 'r') as file:
    for line in file:
        temp = line.split(" ")
        start_state[temp[0]] = temp[1]+" "+temp[2]+" "+temp[3].strip()
        total_count += 1
for i in range(1):
    monte([[i] for i in start_state.keys()])

