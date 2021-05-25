from map import Map
from node import Node
from open_closed import Open, Closed
from distances import *
from consts import *


# AStar with Bounding Boxes

# А* совмещенный с ВВ: если для шага по текущему ребру целевая вершина не попадет в Bounding Box, то этот ход не делаем


def AStarBB(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, weight=1.0, heuristicFunction=EuclidDistance):

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
            e = (i - current.i, j - current.j)
            if gridMap.bb[(current.i, current.j, e)]['r']['min'] > i or gridMap.bb[(current.i, current.j, e)]['r']['max'] < i or gridMap.bb[(current.i, current.j, e)]['c']['min'] > j or gridMap.bb[(current.i, current.j, e)]['c']['max'] < j:
                continue
            if not CLOSED.WasExpanded(neig):
                neig.g = current.g + ComputeCost(current.i, current.j, i, j)
                neig.h = heuristicFunction(i, j, iGoal, jGoal)
                neig.F = neig.g + neig.h * weight
                neig.k = k
                neig.parent = current
                OPEN.AddNode(neig)
        k += 1

    return False, None, CLOSED, OPEN

