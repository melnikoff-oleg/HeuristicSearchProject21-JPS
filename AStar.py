from map import Map
from node import Node
from open_closed import Open, Closed
from distances import *
from consts import *


def AStar(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, weight=1.0, heuristicFunction=EuclidDistance):

    OPEN = Open()
    CLOSED = Closed()
    start = Node(iStart, jStart, 0, heuristicFunction(iStart, jStart, iGoal, jGoal), weight=weight)
    OPEN.AddNode(start)
    
    k = 1
    
    while not OPEN.isEmpty():
        current = OPEN.GetBestNode()
        CLOSED.AddNode(current)

        if current.i == iGoal and current.j == jGoal:
            return True, current, CLOSED, OPEN

        for (i, j) in gridMap.GetNeighbors(current.i, current.j):
            neig = Node(i, j)
            if not CLOSED.WasExpanded(neig):
                neig.g = current.g + ComputeCost(current.i, current.j, i, j)
                neig.h = heuristicFunction(i, j, iGoal, jGoal)
                neig.F = neig.g + neig.h * weight
                neig.k = k
                neig.parent = current
                OPEN.AddNode(neig)
        k += 1

    return False, None, CLOSED, OPEN