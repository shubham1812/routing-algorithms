The below implemented program uses Local Search - Monte Carlo(Partially).                    
Tested with 100 student pref data.                                                           
Cannot guarantee optimal result but on multiple runs it should come close to optimal result. 
State Space: the state space has all the students in it with a maximum of 3 people in a group per state
 We first had to formulate the problem into a search problem for us to use local search. We fist used a BFS algorithm,
 the goal state was defined in such a way that atleast 70% of the students were satisfied and the
cost of error rate was around 20% or less. But this was taking more time for large inputs.
We then modified the goal state that only returns the total cost of the given state and then modified the 
algorithm into a Monte-Carlo local search algorithm which gave us near optimal results when ran for more number of times.
 Initial Sate: It consists of all the students in different groups.
 Successor: This function will always join the first item with the remaining items in the state to generate all possible
 combinations. It also ensures that no state consists of a group size more than 3 and also avoids duplicates. To find an optimal 
 solution, we always need to go to the end of the depth of the node.
 Eg: Consider 3 students: [1][2][3] -> Initial State
                          [[1,2][3]] [[1][2,3]] [[1,3][2]] -> 1st Level
                          [[1,2,3]]                        -> 2nd Level
Cost Function: This function will give a total cost of a state passed using K,M,N values.
