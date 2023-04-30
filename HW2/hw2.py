##############
# Homework 2 #
##############

##############
# Question 1 #
##############

# The funcion BFS takes in an argument FRINGE which represents a list of search trees and
# returns a top-level list of leaf nodes in left-to-right order in tuple. The function is implemented
# with recursion, in which in every recursion nodes at the highest levels are separated from
# the remaining nodes, resulting in two lists. BFS is then recursively called on list with
# lower-level nodes.
def BFS(FRINGE):
    top_level_list = []
    remain = []
    for search_tree in FRINGE:  # separate all nodes into the shallowest layer versus others
        if type(search_tree) is not tuple:
            top_level_list.append(search_tree)
        else:
            for item in search_tree:
                remain.append(item)
    if len(remain) == 0:  # reached the deepest layer of search tree, done
        return tuple(top_level_list)
    return tuple(top_level_list) + BFS(remain)


"""# question 1 test cases
l1 = ("ROOT",)
l2 = (((("L", "E"), "F"), "T"))
l3 = (("R", ("I", ("G", ("H", "T")))))
l4 = ((("A", ("B",)), "C", ("D",)))
l5 = (("T", ("H", "R", "E"), "E"))
l6 = (("A", (("C", (("E",), "D")), "B")))

assert BFS(l1) == ("ROOT",)
assert BFS(l2) == ("T", "F", "L", "E")
assert BFS(l3) == ("R", "I", "G", "H", "T")
assert BFS(l4) == ("C", "A", "D", "B")
assert BFS(l5) == ("T", "E", "H", "R", "E")
assert BFS(l6) == ("A", "B", "C", "D", "E")"""


##############
# Question 2 #
##############


# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).

# The main entry point for this solver is the function DFS, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS returns [].
# To call DFS to solve the original problem, one would call
# DFS((False, False, False, False), [])
# However, it should be possible to call DFS with a different initial
# state or with an initial path.

# First, we define the helper functions of DFS.

# FINAL-STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.

# The function FINAL_STATE is implemented by simply comparing elements of the tuple to boolean expressions.
def FINAL_STATE(S):
    homer, baby, dog, poison = S  # take each element of the tuple
    if homer and baby and dog and poison:
        return True
    return False

# NEXT-STATE returns the state that results from applying an operator to the
# current state. It takes two arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns [].
# NOTE that next-state returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].

# The functin NEXT_STATE is implemented case by case. Inappropriate conditions are checked
# in each case of "h", "b", "d", and "p" and relative update on the state is made.


def NEXT_STATE(S, A):
    homer, baby, dog, poison = S  # current state
    homer_new = not homer  # homer will always move

    if A == "h" and (baby != poison) and (baby != dog):  # only homer move
        return [(homer_new, baby, dog, poison)]

    if A == "b" and (homer == baby):  # homer and baby are on the same side
        baby_new = not baby
        return [(homer_new, baby_new, dog, poison)]

    if A == "d" and (homer == dog):  # homer and dog are on the same side
        dog_new = not dog
        if (baby != poison):
            return [(homer_new, baby, dog_new, poison)]

    if A == "p" and (homer == poison):  # homer and poison are on the same side
        poison_new = not poison
        if (baby != dog):
            return [(homer_new, baby, dog, poison_new)]

    return []


# SUCC-FN returns all of the possible legal successor states to the current
# state. It takes a single argument (s), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.

# The function SUCC_FN utilizes the NEXT_STATE function, basically by passing
# all possible operations to NEXT_STATE and compile the results into a list of tuples.
def SUCC_FN(S):
    operator = ["h", "b", "d", "p"]
    legal_successors = []

    for operation in operator:
        legal_successors += NEXT_STATE(S, operation)

    return legal_successors

# ON-PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if s is a member of
# states and False otherwise.

# The function ON_PATH again does a simple check. Only if S in in the list of STATES
# the function will return true.


def ON_PATH(S, STATES):
    if len(STATES) == 0:
        return False
    if S in STATES:
        return True
    return False


# MULT-DFS is a helper function for DFS. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT-DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT-DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].

# for each set of legal successors inputted, check if there is a goal state and return
# the path, or return []
def MULT_DFS(STATES, PATH):

    if len(STATES) == 0:  # if no more legal successors, return empty path since reached dead end
        return []

    for successor in STATES:
        if FINAL_STATE(successor):
            return PATH + [successor]
        if not ON_PATH(successor, PATH):
            further_successor = SUCC_FN(successor)
            temp_path = MULT_DFS(further_successor, PATH + [successor])
            if temp_path == []:
                pass
            else:
                if FINAL_STATE(temp_path[-1]):
                    return temp_path

    return []

    """# DFS with iteration (including dead end)
    while len(STATES) > 0:  # still states unexplored
        # take last element in the stack of legal successors
        successor = STATES.pop()

        if FINAL_STATE(successor):  # check if reached goal state
            PATH.append(successor)
            return PATH
        # check if already explored, if not generate successors and add to stack, add current node to PATH
        if not ON_PATH(successor, PATH):
            STATES += SUCC_FN(successor)
            PATH.append(successor)

    return []"""


# DFS does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to [] (empty list). DFS
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or empty list [] otherwise. DFS is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path.

# Finally DFS does a precheck on if S is inputted as the goal state
# or if S is an invalid input where it is alreast in PATH. It then call
# on MULT_DFS to give a solution to the problem.
def DFS(S, PATH):

    # check if S is already explored
    if not ON_PATH(S, PATH):
        PATH.append(S)
    # check if S is the goal state
    if FINAL_STATE(S):
        return PATH
    # generate successors of current state
    legal_successors = SUCC_FN(S)
    return MULT_DFS(legal_successors, PATH)


S = (True, True, True, True)
PATH = []
print(DFS(S, PATH))

S = (False, False, False, False)
PATH = []
print(DFS(S, PATH))

S = (False, True, True, False)
PATH = []
print(DFS(S, PATH))
