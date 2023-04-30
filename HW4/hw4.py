##############
# Homework 4 #
##############

# Exercise: Fill this function.
# Returns the index of the variable that corresponds to the fact that
# "Node n gets Color c" when there are k possible colors
#
# The function takes in a node n, a color c, and a list of color 1 to k.
# It returns the converted node index representing the number node n gets
# assigned to. The conversion is done through simple arithmetic.
def node2var(n, c, k):
    return (n - 1) * k + c


# Exercise: Fill this function
# Returns *a clause* for the constraint:
# "Node n gets at least one color from the set {1, 2, ..., k}"
#
# The function takes in a node n and a list of color from 1 to k.
# It returns a single clause in the form of a list. The clause
# specifies node n gets at least one color from color 1 to k, and
# is implemented with disjunction.
def at_least_one_color(n, k):
    clause = []
    for i in range(1, k+1):
        clause.append(node2var(n, i, k))
    return clause


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets at most one color from the set {1, 2, ..., k}"
#
# Having at most one color would mean for every two-pair of colors,
# their propositional logic values cannot be the same. Therefore,
# at most one color should be expressed as NEG(1 AND 2) AND NEG(1 AND 3),
# ... essentially negation of all possible two pairs connected together
# with conjunction. We then convert this into conjunctive normal form:
# (NEG1 OR NEG2) AND (NEG1 OR NEG3) AND ... etc.
def at_most_one_color(n, k):
    CNF = []
    for i in range(1, k+1):
        index = node2var(n, i, k)
        for j in range(i+1, k+1):
            CNF.append([-index, -node2var(n, j, k)])
    return CNF


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Node n gets exactly one color from the set {1, 2, ..., k}"
#
# Node n gets exactly one color when it satifies both statements
# "node n gets at least one value" and "node n gets at most one value."
# Therefore by connecting two statements with conjunction we obtain
# statement for node n getting exactly one color.
def generate_node_clauses(n, k):
    clause_list = []
    clause_list.append(at_least_one_color(n, k))

    at_most = at_most_one_color(n, k)
    for clause in at_most:
        clause_list.append(clause)
    return clause_list


# Exercise: Fill this function
# Returns *a list of clauses* for the constraint:
# "Nodes connected by an edge e (represented by a list)
# cannot have the same color"
#
# For any two nodes, we write NEG(X AND Y) to represent
# node X and node Y cannot have the same value/color. We then
# convert this negation to a conjunctive normal form.
def generate_edge_clauses(e, k):
    edge_clause_list = []
    for i in range(1, k+1):
        index_x = node2var(e[0], i, k)
        index_y = node2var(e[1], i, k)
        edge_clause_list.append([-index_x, -index_y])
    return edge_clause_list


# The function below converts a graph coloring problem to SAT
# DO NOT MODIFY
def graph_coloring_to_sat(graph_fl, sat_fl, k):
    clauses = []
    with open(graph_fl) as graph_fp:
        node_count, edge_count = tuple(map(int, graph_fp.readline().split()))
        for n in range(1, node_count + 1):
            clauses += generate_node_clauses(n, k)
        for _ in range(edge_count):
            e = tuple(map(int, graph_fp.readline().split()))
            clauses += generate_edge_clauses(e, k)
    var_count = node_count * k
    clause_count = len(clauses)
    with open(sat_fl, 'w') as sat_fp:
        sat_fp.write("p cnf %d %d\n" % (var_count, clause_count))
        for clause in clauses:
            sat_fp.write(" ".join(map(str, clause)) + " 0\n")


# Example function call
if __name__ == "__main__":
    graph_coloring_to_sat("graph2.txt", "graph2_8colors.txt", 8)
