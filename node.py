# Node representation
# Node class represents a search node

# - i, j: coordinates of corresponding grid element
# - g: g-value of the node
# - h: h-value of the node
# - F: f-value of the node
# - parent: pointer to the parent-node 
# - startingNodeEdgesMask: mask of initial edges from starting vertex, from which we can get to current vertex optimally


class Node:
    def __init__(self, i, j, g = 0, h = 0, F = None, parent = None, k=0, weight=1.0):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        self.startingNodeEdgesMask = 0
        if F is None:
            self.F = self.g + h * weight
        else:
            self.F = F        
        self.parent = parent
    
    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)
    
    def __str__(self):
        return 'Node i={} j={}, g={} F={}'.format(self.i, self.j, self.g, self.F)
    
    def __lt__(self, other):
        return self.F < other.F\
        or ((self.F == other.F) and (self.h < other.h))\
        or ((self.F == other.F) and (self.h == other.h) and (self.k > other.k))
