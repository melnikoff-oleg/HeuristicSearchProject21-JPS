from map import Map
from node import Node
from open_closed import Open, Closed
from distances import *
from consts import *

def BJPS(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, heuristicFunction=DiagonalDistance, b=-1):
    OPEN = Open()
    CLOSED = Closed()
    OPEN.AddNode(Node(iStart, jStart, g=0, h=heuristicFunction(iStart, jStart, iGoal, jGoal)))
    
    pathFound = False
    node = None
    
    k = 1
    
    while not OPEN.isEmpty():
        node = OPEN.GetBestNode()
        i, j = node.i, node.j
        if (i, j) == (iGoal, jGoal):
            pathFound = True
            break
        for i1, j1 in gridMap.GetSuccessors(node, Node(iGoal, jGoal), limit=b):
            neighbor = Node(i=i1,
                            j=j1, 
                            g=node.g + ComputeCost(i, j, i1, j1),
                            h=heuristicFunction(i1, j1, iGoal, jGoal),
                            k=k,
                            parent=node
            )
            if CLOSED.WasExpanded(neighbor):
                continue
            OPEN.AddNode(neighbor)
        CLOSED.AddNode(node)
        k += 1
        
    return pathFound, node, CLOSED, OPEN


def JPS(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, heuristicFunction=DiagonalDistance):
    return BJPS(gridMap, iStart, jStart, iGoal, jGoal, heuristicFunction=heuristicFunction, b=-1)