##############
# Homework 3 #
##############


###################
# Read This First #
###################


# All functions that you need to modify are marked with 'EXERCISE' in their header comments.
# Do not modify astar.py
# This file also contains many helper functions. You may call any of them in your functions.


# Due to the memory limitation, the A* algorithm may crash on some hard sokoban problems if too many
# nodes are generated. Improving the quality of the heuristic will mitigate
# this problem, as it will allow A* to solve hard problems with fewer node expansions.


# Remember that most functions are not graded on efficiency (only correctness).
# Efficiency can only influence your heuristic performance in the competition (which will affect your score).


# Load the astar.py and do not modify it.
import astar
# Load the numpy package and the state is represented as a numpy array during this homework.
import numpy as np


# a_star perform the A* algorithm with the start_state (numpy array), goal_test (function), successors (function) and
# heuristic (function). a_star prints the solution from start_state to goal_state (path), calculates the number of
# generated nodes (node_generated) and expanded nodes (node_expanded), and the solution depth (len(path)-1). a_star
# also provides the following functions for printing states and moves: prettyMoves(path): Translate the solution to a
# list of moves printlists(path): Visualize the solution and Print a list of states
def a_star(start_state, goal_test, successors, heuristic):
    goal_node, node_generated, node_expanded = astar.a_star_search(
        start_state, goal_test, successors, heuristic)
    if goal_node:
        node = goal_node
        path = [node.state1]
        while node.parent:
            node = node.parent
            path.append(node.state1)
        path.reverse()

        # print('My path:{}'.format(path))
        # print(prettyMoves(path))
        # printlists(path)
        print('Nodes Generated by A*: {}'.format(node_generated))
        print('Nodes Expanded by A*: {}'.format(node_expanded))
        print('Solution Depth: {}'.format(len(path) - 1))
    else:
        print('no solution found')


# A shortcut function
# Transform the input state to numpy array. For other functions, the state s is presented as a numpy array.
# Goal-test and next-states stay the same throughout the assignment
# You can just call sokoban(init-state, heuristic function) to test the result
def sokoban(s, h):
    return a_star(np.array(s), goal_test, next_states, h)


# Define some global variables
blank = 0
wall = 1
box = 2
keeper = 3
star = 4
boxstar = 5
keeperstar = 6


# Some helper functions for checking the content of a square
def isBlank(v):
    return (v == blank)


def isWall(v):
    return (v == wall)


def isBox(v):
    return (v == box)


def isKeeper(v):
    return (v == keeper)


def isStar(v):
    return (v == star)


def isBoxstar(v):
    return (v == boxstar)


def isKeeperstar(v):
    return (v == keeperstar)


# Help function for get KeeperPosition
# Given state s (numpy array), return the position of the keeper by row, col
# The top row is the zeroth row
# The first (right) column is the zeroth column
def getKeeperPosition(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            if (isKeeper(s[i, j]) or isKeeperstar(s[i, j])):
                return i, j


# For input list s_list, remove all None element
# For example, if s_list = [1, 2, None, 3], returns [1, 2, 3]
def cleanUpList(s_list):
    clean = []
    for state in s_list:
        if state is not None:
            clean.append(state)
    return clean


# EXERCISE: Modify this function to return Ture
# if and only if s (numpy array) is a goal state of a Sokoban game.
# (no box is on a non-goal square)
# Remember, the number of goal can be larger than the number of box.
# Currently, it always returns False. If A* is called with
# this function as the goal testing function, A* will never
# terminate until the whole search space is exhausted.

# goal_test takes in a state s and determines if it is the goal state.
# It iterates through every square in the state s. As long as we can find
# one box that is not on the goal, goal_test(s) returns false.
# In all other cases it returns true.
def goal_test(s):
    # get shape of our board
    row = s.shape[0]
    col = s.shape[1]

    # iterate through the state
    for i in range(row):
        for j in range(col):
            if isBox(s[i, j]):
                return False

    # if there is no box not on a goal, we reached the goal state
    return True


# get_square is a helper function for try_move(s, d).
# It takes in a state s, an integer representing row number
# and an integer representing column number as arguments. It returns the integer
# content of state s at the coordinate (r,c). (r,c) starts from (0,0) at the upper
# left corner of the board. If the inputted r,c values are not within the board,
# the function returns the integer content of a wall. Nothing is modified in this function.
def get_square(s, r, c):

    # valid r values fall in [0, s.shape[0]-1] because of indexing
    if r < 0 or r >= s.shape[0]:
        return 1
    # valid c values fall in [0, s.shape[1]-1] because of indexing
    if c < 0 or c >= s.shape[1]:
        return 1
    return s[r, c]


# set_square is a helper function for try_move(s, d).
# It takes in a state s, a row number r, a column number c, and an integer content v.
# It returns a new state s_prime where the content at coordinate [r,c] of s_prime is set to v with the
# rest of the contents the same as s. The original state s, is not modified in this function.
def set_square(s, r, c, v):
    s_prime = np.copy(s)  # make a copy of s
    s_prime[r, c] = v
    return s_prime


# update_position is a helper function for try_move(s, d).
# It takes in a row number r, a column number c, and a direction d. It returns
# the updated grid position in row and column by moving one step in the direction specified
# by d. update_position does not modify the original inputted coordinate r and c.
def update_position(r, c, d):

    if d == "u" or d == "d":
        new_c = np.copy(np.array(c))  # prevent same reference issue
    elif d == "l" or d == "r":
        new_r = np.copy(np.array(r))  # prevent same reference issue

    if d == "u":
        new_r = r - 1
    if d == "d":
        new_r = r + 1
    if d == "l":
        new_c = c - 1
    if d == "r":
        new_c = c + 1

    return new_r, new_c


# valid_move is a helper function for try_move(s, d).
# It takes in a state s, a row number r, a column number c, and a direction d. It evaluates whether
# moving one grid in d direction to s[r,c] is a valid move or not. Here s[r,c] represents the grid the keeper
# wish to move into. There are two cases where such move would not be valid:
# 1. if s[r,c] is a wall,
# 2. if s[r,c] is a box or box+goal, have to think about if the box can be pushed along that direction further
# The function returns true only when the move is valid.
def valid_move(s, r, c, d):

    content = get_square(s, r, c)  # what is on that grid

    if isWall(content):  # a wall, invalid
        return False
    # a box or a box on the goal, have to look at one grid in d direction further
    if isBox(content) or isBoxstar(content):
        r_further, c_further = update_position(r, c, d)
        content = get_square(s, r_further, c_further)
        if isWall(content) or isBox(content) or isBoxstar(content):
            return False
    return True


# try_move is a helper function for next_state(s).
# It takes a current state s and a direction d, and tries to make a move at direction d for the keeper.
# The inputted state s here will be a copy of the current state. It checks if the move is valid, and if it is
# not, the function returns none. If the move is valid, then it goes ahead and modify contents of grids involved
# in the move accordingly. For each move tried, at most 3 grids will be modified.
def try_move(s, d):

    # get keeper position
    row, col = getKeeperPosition(s)
    orig_keeper = get_square(s, row, col)

    # the grid the keeper want to move into
    test_row, test_col = update_position(row, col, d)

    # if the move is valid, return the new state
    if valid_move(s, test_row, test_col, d):

        # update the grid where the keeper used to be

        # if the original keeper position is only the keeper, after the keeper moved it should become a blank
        if isKeeper(orig_keeper):
            s = set_square(s, row, col, 0)
         # if the original keeper position is the keeper and the goal, after the keeper moved it should become a goal
        elif isKeeperstar(orig_keeper):
            s = set_square(s, row, col, 4)

        # update the grid where the keeper is now moving into
        moveinto = get_square(s, test_row, test_col)

        # if the grid moves into is blank, set it to keeper
        if isBlank(moveinto):
            s = set_square(s, test_row, test_col, 3)
        # if the grid moves into is a goal, set it to keeper+goal
        elif isStar(moveinto):
            s = set_square(s, test_row, test_col, 6)
        # otherwise a third grid needs to be modified
        else:
            test_row_2, test_col_2 = update_position(test_row, test_col, d)
            pushinto = get_square(s, test_row_2, test_col_2)
            # if the grid moves into is a box, set it to keeper
            if isBox(moveinto):
                s = set_square(s, test_row, test_col, 3)
            # if the grid moves into is a box+goal, set it to keeper+goal
            elif isBoxstar(moveinto):
                s = set_square(s, test_row, test_col, 6)

            # if the grid the box being pushed into is blank, set it to box
            if isBlank(pushinto):
                s = set_square(s, test_row_2, test_col_2, 2)
            # if the grid the box being pushed into is a goal, set it to box+goal
            elif isStar(pushinto):
                s = set_square(s, test_row_2, test_col_2, 5)

        return s

    # if not a valid move, return None
    return None


# EXERCISE: Modify this function to return the list of
# successor states of s (numpy array).

# This is the top-level next-states (successor) function.
# Some skeleton code is provided below.
# You may delete them totally, depending on your approach.
#
# If you want to use it, you will need to set 'result' to be
# the set of states after moving the keeper in each of the 4 directions.
#
# You can define the function try-move and decide how to represent UP,DOWN,LEFT,RIGHT.
# Any None result in the list can be removed by cleanUpList.
#
# When generated the successors states, you may need to copy the current state s (numpy array).
# A shallow copy (e.g, direcly set s1 = s) constructs a new compound object and then inserts references
# into it to the objects found in the original. In this case, any change in the numpy array s1 will also affect
# the original array s. Thus, you may need a deep copy (e.g, s1 = np.copy(s)) to construct an indepedent array.

# next_state takes in a state s and returns the list of valid successor states. It calls try_move
# in each of four directions, and append the resulting states to a list. Each time within the for
# loop, a new copy of the state s will be created so that states are not confused. Finally if there
# are any none states in the list, they get eliminated by cleanUpList().
def next_states(s):
    s_list = []
    directions = ["u", "d", "l", "r"]

    # Move the keeper in U,D,L,R four directions and record successor states
    for direction in directions:
        s1 = np.copy(s)
        s_list.append(try_move(s1, direction))

    return cleanUpList(s_list)


# EXERCISE: Modify this function to compute the trivial
# admissible heuristic.

# The function simply returns 0, which is always an admissible heuristic since 0 is
# always smaller than the lowest possible cost from the current state to the goal state.
def h0(s):
    return 0


# EXERCISE: Modify this function to compute the
# number of misplaced boxes in state s (numpy array).

# h1 function takes in a state and iterate through the game
# board to find boxes that are not on the goal. This is done
# by incrementing count whenever there is one such box found.
# This is an admissible heuristic because when there are n boxes left
# that are not yet on the goal, the lowest possible cost from the current
# state to reach the goal state would be at least n moves, with each move
# sending one box into a goal grid in the ideal condition. So h1(s) never
# overestimates the lowest possible cost.
def h1(s):
    # get shape
    row = s.shape[0]
    col = s.shape[1]

    count = 0

    # iterate through the state, if find an alone box
    # not on the goal, increment count by 1
    for i in range(row):
        for j in range(col):
            if isBox(s[i, j]):
                count += 1

    return count


# EXERCISE: Change the name of this function to h<UID> where
# <UID> is your actual student ID number. Then, modify this
# function to compute an admissible heuristic value of s.
# For example, if my UID is 123456789, then I should change the function name to 'h123456789'
# This function will be tested in various hard examples.
# Objective: make A* solve problems as fast as possible.

# The deadend function is a helper function for heuristic h405312725. It takes in a state s,
# a row number and a column number representing the position of a box, and returns whether
# this is a dead box stuck in some corner and cannot be moved anymore. For example if there
# exists a box in the lower left corner of the board or be surrounded by walls both below
# and to the left, this box cannot be moved anymore. Thus creating a dead box and the state
# is insolvable.
def deadend(s, r, c):
    dead_upper = (r == 0) or isWall(s[r-1, c])
    dead_lower = (r == s.shape[0] - 1) or isWall(s[r+1, c])
    dead_left = (c == 0) or isWall(s[r, c-1])
    dead_right = (c == s.shape[1] - 1) or isWall(s[r, c+1])

    return (dead_upper or dead_lower) and (dead_left or dead_right)


# The function h405312725 takes in a state s and returns an integer >= 0. The integer
# returned is used as heuristic in the A* search algorithm. There are two cases:
# 1. If we encounter a dead box as explained in the deadend(s,r,c) function, then
#    we return a large number immediately since we are stuck in a dead state.
#    This would be admissible because in the case of a dead state, the lowest possible
#    cost from current state to the goal state would be infinite. And a large number < infinity.
# 2. The heuristic is calculated by first finding the shortest manhattan distance to one of the remaining goals for each box,
#    and then summing up all those shortest distances. This is an admissible heuristic because
#    for each box, we look over all remaining goals, calculate manhattan distances, and take the shortest
#    distance, which means for each box we never overestimate the lowest possible path cost for it to reach
#    a goal. The same reasoning applies to all shortest distances found and when these distances are
#    summed up, it should not overestimate the lowest possible path cost from the currrent state
#    to push all boxes into goals.
def h405312725(s):
    row = s.shape[0]
    col = s.shape[1]

    shortest_distance = 0
    box_position = []
    goal_position = []

    # capture coordinate of all unassigned boxes and stars
    for i in range(row):
        for j in range(col):
            if isBox(s[i, j]):
                if deadend(s, i, j):  # if meet a box stuck in a corner, return a really big number
                    return 10000
                box_position.append([i, j])
            elif isStar(s[i, j]) or isKeeperstar(s[i, j]):
                goal_position.append([i, j])
    # if no box unassigned return 0
    if not box_position:
        return shortest_distance
    # for each box find the shortest manhattan distance to a goal
    for box in box_position:
        distance = []
        for goal in goal_position:
            distance.append(abs(box[0]-goal[0]) + abs(box[1]-goal[1]))
        shortest_distance += min(distance)

    return shortest_distance


# Some predefined problems with initial state s (array). Sokoban function will automatically transform it to numpy
# array. For other function, the state s is presented as a numpy array. You can just call sokoban(init-state,
# heuristic function) to test the result. Each problem can be visualized by calling prettyMoves(path) and printlists(
# path) in a_star function
#
# Problems are roughly ordered by their difficulties.
# For most problems, we also provide 2 additional number per problem:
#    1) # of nodes expanded by A* using our next-states and h0 heuristic.
#    2) the depth of the optimal solution.
# These numbers are located at the comments of the problems. For example, the first problem below
# was solved by 80 nodes expansion of A* and its optimal solution depth is 7.
#
# Your implementation may not result in the same number of nodes expanded, but it should probably
# give something in the same ballpark. As for the solution depth, any admissible heuristic must
# make A* return an optimal solution. So, the depths of the optimal solutions provided could be used
# for checking whether your heuristic is admissible.
#
# Warning: some problems toward the end are quite hard and could be impossible to solve without a good heuristic!


# [80,7]
s1 = [[1, 1, 1, 1, 1, 1],
      [1, 0, 3, 0, 0, 1],
      [1, 0, 2, 0, 0, 1],
      [1, 1, 0, 1, 1, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1]]

# [110,10],
s2 = [[1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 0, 0, 0, 1],
      [1, 0, 0, 2, 1, 4, 1],
      [1, 3, 0, 0, 1, 0, 1],
      [1, 1, 1, 1, 1, 1, 1]]

# [211,12],
s3 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 2, 0, 3, 4, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [300,13],
s4 = [[1, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 0, 0, 1, 4],
      [0, 0, 0, 0, 0, 0, 0],
      [0, 0, 1, 1, 1, 0, 0],
      [0, 0, 1, 0, 0, 0, 0],
      [0, 2, 1, 0, 0, 0, 0],
      [0, 3, 1, 0, 0, 0, 0]]

# [551,10],
s5 = [[1, 1, 1, 1, 1, 1],
      [1, 1, 0, 0, 1, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 4, 2, 2, 4, 1],
      [1, 0, 0, 0, 0, 1],
      [1, 1, 3, 1, 1, 1],
      [1, 1, 1, 1, 1, 1]]

# [722,12],
s6 = [[1, 1, 1, 1, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 4, 1],
      [1, 0, 0, 0, 2, 2, 3, 1],
      [1, 0, 0, 1, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1, 1, 1]]

# [1738,50],
s7 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 1, 1, 1, 1, 0, 0, 0, 3],
      [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
      [0, 2, 1, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 0, 0, 0, 1, 4]]

# [1763,22],
s8 = [[1, 1, 1, 1, 1, 1],
      [1, 4, 0, 0, 4, 1],
      [1, 0, 2, 2, 0, 1],
      [1, 2, 0, 1, 0, 1],
      [1, 3, 0, 0, 4, 1],
      [1, 1, 1, 1, 1, 1]]

# [1806,41],
s9 = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 0, 0, 1, 1, 1, 1],
      [1, 0, 0, 0, 0, 0, 2, 0, 1],
      [1, 0, 1, 0, 0, 1, 2, 0, 1],
      [1, 0, 4, 0, 4, 1, 3, 0, 1],
      [1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [10082,51],
s10 = [[1, 1, 1, 1, 1, 0, 0],
       [1, 0, 0, 0, 1, 1, 0],
       [1, 3, 2, 0, 0, 1, 1],
       [1, 1, 0, 2, 0, 0, 1],
       [0, 1, 1, 0, 2, 0, 1],
       [0, 0, 1, 1, 0, 0, 1],
       [0, 0, 0, 1, 1, 4, 1],
       [0, 0, 0, 0, 1, 4, 1],
       [0, 0, 0, 0, 1, 4, 1],
       [0, 0, 0, 0, 1, 1, 1]]

# [16517,48],
s11 = [[1, 1, 1, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 4, 1],
       [1, 0, 2, 2, 1, 0, 1],
       [1, 0, 2, 0, 1, 3, 1],
       [1, 1, 2, 0, 1, 0, 1],
       [1, 4, 0, 0, 4, 0, 1],
       [1, 1, 1, 1, 1, 1, 1]]

# [22035,38],
s12 = [[0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
       [1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
       [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 2, 1, 1, 1, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 1, 0, 1, 4, 0, 4, 1],
       [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]]

# [26905,28],
s13 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 0, 0, 2, 0, 1],
       [1, 0, 2, 0, 0, 0, 0, 0, 4, 1],
       [1, 0, 3, 0, 0, 0, 0, 0, 2, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 0, 4, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

# [41715,53],
s14 = [[0, 0, 1, 0, 0, 0, 0],
       [0, 2, 1, 4, 0, 0, 0],
       [0, 2, 0, 4, 0, 0, 0],
       [3, 2, 1, 1, 1, 0, 0],
       [0, 0, 1, 4, 0, 0, 0]]

# [48695,44],
s15 = [[1, 1, 1, 1, 1, 1, 1],
       [1, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 2, 2, 0, 1],
       [1, 0, 2, 0, 2, 3, 1],
       [1, 4, 4, 1, 1, 1, 1],
       [1, 4, 4, 1, 0, 0, 0],
       [1, 1, 1, 1, 0, 0, 0]]

# [91344,111],
s16 = [[1, 1, 1, 1, 1, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0],
       [1, 2, 1, 0, 1, 1, 1, 1],
       [1, 4, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 5, 0, 5, 0, 1],
       [1, 0, 5, 0, 1, 0, 1, 1],
       [1, 1, 1, 0, 3, 0, 1, 0],
       [0, 0, 1, 1, 1, 1, 1, 0]]

# [3301278,76],
# Warning: This problem is very hard and could be impossible to solve without a good heuristic!
s17 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 3, 0, 0, 1, 0, 0, 0, 4, 1],
       [1, 0, 2, 0, 2, 0, 0, 4, 4, 1],
       [1, 0, 2, 2, 2, 1, 1, 4, 4, 1],
       [1, 0, 0, 0, 0, 1, 1, 4, 4, 1],
       [1, 1, 1, 1, 1, 1, 0, 0, 0, 0]]

# [??,25],
s18 = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 4, 1, 0, 0, 0, 0]]

# [??,21],
s19 = [[0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2, 0],
       [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 4],
       [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 1, 0, 2, 0, 4, 1, 0, 0, 0]]


# Utility functions for printing states and moves.
# You do not need to understand any of the functions below this point.


# Helper function of prettyMoves
# Detect the move from state s --> s1
def detectDiff(s, s1):
    row, col = getKeeperPosition(s)
    row1, col1 = getKeeperPosition(s1)
    if (row1 == row + 1):
        return 'Down'
    if (row1 == row - 1):
        return 'Up'
    if (col1 == col + 1):
        return 'Right'
    if (col1 == col - 1):
        return 'Left'
    return 'fail'


# Translates a list of states into a list of moves
def prettyMoves(lists):
    initial = 0
    action = []
    for states in (lists):
        if (initial != 0):
            action.append(detectDiff(previous, states))
        initial = 1
        previous = states
    return action


# Print the content of the square to stdout.
def printsquare(v):
    if (v == blank):
        print(' ', end='')
    if (v == wall):
        print('#', end='')
    if (v == box):
        print('$', end='')
    if (v == keeper):
        print('@', end='')
    if (v == star):
        print('.', end='')
    if (v == boxstar):
        print('*', end='')
    if (v == keeperstar):
        print('+', end='')


# Print a state
def printstate(s):
    row = s.shape[0]
    col = s.shape[1]
    for i in range(row):
        for j in range(col):
            printsquare(s[i, j])
        print('\n')


# Print a list of states with delay.
def printlists(lists):
    for states in (lists):
        printstate(states)
        print('\n')


"""# testing next_state(s)
s1 = [[1, 1, 1, 1, 1],
      [1, 0, 0, 4, 1],
      [1, 0, 2, 0, 1],
      [1, 0, 3, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]]

s2 = [[1, 1, 1, 1, 1],
      [1, 0, 0, 4, 1],
      [1, 0, 2, 3, 1],
      [1, 0, 0, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]]"""

"""# testing goal_test(s)
g1 = [[1, 1, 1, 1, 1],
      [1, 5, 0, 4, 1],
      [1, 0, 2, 0, 1],
      [1, 0, 3, 5, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]]

g2 = [[1, 1, 1, 1, 1],
      [1, 0, 0, 4, 1],
      [1, 0, 5, 0, 1],
      [1, 0, 3, 0, 1],
      [1, 0, 0, 0, 1],
      [1, 1, 1, 1, 1]]"""


if __name__ == "__main__":

    """sokoban(s1, h0)
    sokoban(s2, h0)
    sokoban(s3, h0)
    sokoban(s4, h0)
    sokoban(s5, h0)
    sokoban(s6, h0)
    sokoban(s13, h0)
    sokoban(s14, h0)
    sokoban(s16, h0)"""

    """sokoban(s1, h1)
    sokoban(s2, h1)
    sokoban(s3, h1)
    sokoban(s4, h1)
    sokoban(s5, h1)
    sokoban(s6, h1)"""

    # Nodes Generated by A*: 8940426; Nodes Expanded by A*: 3346738; Solution Depth: 76
    #sokoban(s17, h0)

    # Nodes Generated by A*: 8458565; Nodes Expanded by A*: 3167311; Solution Depth: 76
    #sokoban(s17, h1)

    # Nodes Generated by A*: 1444024; Nodes Expanded by A*: 536575; Solution Depth: 76
    sokoban(s17, h405312725)

    # all test cases give correct optimal depth
    """sokoban(s1, h405312725)
    sokoban(s2, h405312725)
    sokoban(s3, h405312725)
    sokoban(s4, h405312725)
    sokoban(s5, h405312725)
    sokoban(s6, h405312725)
    sokoban(s7, h405312725)
    sokoban(s8, h405312725)"""
    """sokoban(s9, h405312725)
    sokoban(s10, h405312725)
    sokoban(s11, h405312725)
    sokoban(s12, h405312725)
    sokoban(s13, h405312725)
    sokoban(s14, h405312725)
    sokoban(s15, h405312725)
    sokoban(s16, h405312725)"""
    #sokoban(s18, h405312725)
    #sokoban(s19, h405312725)

    """list_test = next_states(np.array(s1))
    print(list_test)

    list_test_2 = next_states(np.array(s2))
    print(list_test_2)"""

    """print(goal_test(np.array(g1)))
    print(goal_test(np.array(g2)))"""
