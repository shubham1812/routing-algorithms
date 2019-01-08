#!/bin/python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
# modified by araghuv-sgodshal-rojraman
#########################################################################################################
#Problem Statement
#
#Initial State S0 = game board consisting of a 4x4 grid, but with
#no empty space, so there are 16 tiles instead of 15.
#
#State Space S: A valid state is one that has tiles 1 to 16. Given that state must be solvable to be a valid state. 
#
#Successor Function S' = The valid successor in this problem is form after choosinng a row of
#the puzzle and sliding the entire row of tiles left or right, with the left- or right-most tile wrapping around
#to the other side of the board, or choosing a column of the puzzle and sliding the entire the column up or
#down, with the top- or bottom-most tile wrapping around.
#
#Edge Weight : each move will cost 1 unit
#
#Goal State :
#            1 2 3 4
#            5 6 7 8
#            9 10 11 12
#            13 14 15 16
#
#Implemented A* Search with suitable algorithm to solve this problem
#
#Heuristic used:
#1.  Circular Manhattan distane - Refer heuristic - This was found admissable when compared to the other heuristics.
#2.  Manhattan distance with linear conflict - 
#######################################################################################################################


from Queue import PriorityQueue
from random import randrange, sample
import sys
import string

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*4):(row*4+4)] 
    successor_state = state[:(row*4)] + change_row[-dir:] + change_row[:-dir] + state[(row*4+4):]
    return ( successor_state, ("L" if dir == -1 else "R") + str(row+1)  )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print '%3d %3d %3d %3d' % (row[j:(j+4)])

# return a list of possible successor states
def successors(state):
    return [ shift_row(state, i, d) for i in range(0,4) for d in (1,-1) ] + [ shift_col(state, i, d) for i in range(0,4) for d in (1,-1) ] 

# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)
    
def heuristic(state):
    count = 0
    for x in range(0,len(state)):
        if x+1 != state[x]:
            count+=1
    return count

def calculate_man(state):
    sum = 0
    for k in range(len(state)):
        sum +=(abs(state.index(k+1) - k))
    return sum

def heuristic_1(state):
    count = 0
    for i in range(16):
            sum_col = 0
            sum_row = 0
    if(i%4 == 0):
            counter_column = 0
            while(counter_column < 4):
                    if((counter_column+i) != state.index(counter_column+i+1)):
                            sum_col = sum_col + 1
                    counter_column += 1
    if(sum_col > 2):
            count += 1
            sum_col = 0
    if(sum_row > 2):
            count += 1
            sum_row = 0
    if(i != state.index(i+1)):
            sum_row += 1
    return count

#center position 
def center_position_heuristic(state):
    sum = 0
    max_value = sys.maxint
    left_value = max_value
    right_value = max_value
    top_value = max_value
    bottom_value = max_value
    for k in range(len(state)):
        if k%4 == 0:
            left_value = 0 
        if k/4 == 0 :
            top_value = 0 
        if k/4 ==3 :
            bottom_value = 0
        if k%4 == 3:
            right_value = 0 

        if right_value == max_value:
            right_value = state[k] - state[k+1]
        if top_value == max_value:
            top_value = state[k] - state[k-4]
        if left_value == max_value:
            left_value = state[k] - state[k-1]
        if bottom_value == max_value:
            bottom_value = state[k] - state[k+4]

        sum +=left_value +right_value + bottom_value +top_value
    return sum

#manhattan distance
def manhattan_distance_heuristic_with_linear_conflict(state):
    heuristic = 0;
    for x in range(len(state)):
        value = state[x];        
        targetX = (value - 1) / 4;
        targetY = (value - 1) % 4;
        dx = x/4 - targetX;
        dy = x%4 - targetY;
        heuristic += (abs(dx) + abs(dy)) / 6.0; 
    return heuristic
    
#Linear conflict 
def linear_conflict(state):
    heuristic=0
    for x in range(0,len(state)):
        if (state[x]-1)/4 == x/4 : 
            for k in range(x+1, 4 if (x/4) == 0 else 4+4*(x/4)):
                if (state[k]-1)/4 == k/4:
                    if state[k] < state[x]:
                        heuristic+=2

    for x in range(len(state)):
        if (state[x]-1)%4 == x%4: 
            for k in range(x+4, 16, 4):
                if (state[k] - 1)%4 == k%4:
                    if state[k] < state[x]:
                        heuristic +=2
    return heuristic

#heuristic for circular manhattan
def heuristic(state):
    sum = 0
    for k in range(0,len(state)):
        sum +=(1 if (abs(state.index(k+1)/4 - k/4) ) == 3 else (abs(state.index(k+1)/4 - k/4) ))+ (1 if (abs(state.index(k+1)%4 - k%4))==3 else (abs(state.index(k+1)%4 - k%4)) )
    return sum

# The solver! - using BFS right now
def solve(initial_board):
    fringe = PriorityQueue()
    fringe.put((heuristic(initial_board),(initial_board, "")))
    while not fringe.empty() :
        (priority,(state, route_so_far)) = fringe.get()
        for (succ, move) in successors( state ):
            if is_goal(succ):
                return( route_so_far + " " + move )
            fringe.put((heuristic(succ) + len(route_so_far) , (succ, route_so_far + " " + move ))) 
    return False

# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [ int(i) for i in line.split() ]

if len(start_state) != 16:
    print "Error: couldn't parse start state file"

print "Start state: "
print_board(tuple(start_state))

print "Solving..."
route = solve(tuple(start_state))

print "Solution found in " + str(len(route)/3) + " moves:" + "\n" + route