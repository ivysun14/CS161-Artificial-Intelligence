# QUESTION 1
# The function takes in a single integer argument N >= 0 and returns the value of the Nth Padovan number.
# The function is implemented with recursion where the base cases are N = 0 or N = 1 or N = 2,
# in which case the Padovan numbers in the sequence are both 1.  The recursion builds on these base cases
# and calculates the other Padovan numbers in the sequence by breaking the problem into smaller pieces
# with the relation PAD(N) = PAD(N-2)+PAD(N-3).
def PAD(N):
    if (N == 0) or (N == 1) or (N == 2):
        return 1
    return PAD(N-2)+PAD(N-3)

# question 1 test function


def test():
    padovanNumber = [1, 1, 1, 2, 2, 3, 4, 5, 7, 9]
    result = []
    isCorrect = False
    for i in range(0, 10):
        result.append(PAD(i))
    if result == padovanNumber:
        isCorrect = True
    return isCorrect


'''
passTest = test()
print(passTest)
print(PAD(20))
print(PAD(50))
print(PAD(80))
print(PAD(100))
'''

# QUESTION 2
# The function takes in a single integer argument N >= 0 and returns the number of additions
# needed for the PAD(N) function to output the Nth Padovan number.
# The function is implemented with recursion. Similarly, the base cases of the recursion
# are N = 0 or N = 1 or N = 2, since the first third Padovan number in the
# sequence can be outputted as 1 without addition. Afterwards, number of additions are calculated
# with SUMS(N) = SUMS(N-2)+SUMS(N-3)+1, since with each level deeper in the recursion,
# the number of addition plus 1.


def SUMS(N):
    if (N == 0) or (N == 1) or (N == 2):
        return 0
    else:
        return SUMS(N-2)+SUMS(N-3)+1

# question 2 test function


def test_two():
    padovanAddition = [0, 0, 0, 1, 1, 2, 3, 4, 6, 8]
    numberSum = []
    isCorrect = False
    for i in range(0, 10):
        numberSum.append(SUMS(i))
    if numberSum == padovanAddition:
        isCorrect = True
    return isCorrect


'''
passTest2 = test_two()
print(passTest2)
'''

# QUESTION 3
# The function takes in a tree, which can be represented as a tuple or in the case
# of a single leaf node simply a non-tuple object. The function outputs a tree represented
# in tuple with the exact same structure while all nodes are replaced with symbol "?".
# Again the function is implemented with recursion which unpacks the tuple by subtree.
# The base case is when there is only one node left in a subtree, and we know this because
# with only one node left the type of the node is not "tuple." To deal with index error when
# length of any tuple is zero return an empty tuple. Finally the recursion works by unpacking
# the tree into subtrees following the order in the original tuple.


def ANON(TREE):
    if type(TREE) != tuple:
        return "?"
    if len(TREE) == 0:
        return ()
    return (ANON(TREE[0]),) + ANON(TREE[1:])


'''
item = 42
print(ANON(item))
item = "FOO"
print(ANON(item))
item = ((("L", "E"), "F"), "T")
print(ANON(item))
item = ((5, "FOO", 3.1, -0.2))
print(ANON(item))
item = ((1, ("FOO", 3.1), -0.2))
print(ANON(item))
item = ((((1, 2), ("FOO", 3.1)), ("BAR", -0.2)))
print(ANON(item))
item = (("R", ("I", ("G", ("H", "T")))))
print(ANON(item))
'''
