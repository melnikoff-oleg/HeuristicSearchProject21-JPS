from map import Map
from node import Node
from open_closed import Open, Closed
from distances import *
from consts import *





# Реализация алгоритма Дейкстры, которая будет нужна нам во время предподсчета Bounding Boxes.

# В отличии от обычной Дейкстры, тут мы для каждой вершины храним 8-битную маску того, по каким ребрам можно выйти из стартовой вершины, чтобы дойти до текущей оптимальным путем



def Dijkstra8bit(gridMap : Map, iStart : int, jStart : int, iGoal : int, jGoal : int, weight=0, heuristicFunction=EuclidDistance):

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
            if not CLOSED.WasExpanded(neig):
                neig.g = current.g + ComputeCost(current.i, current.j, i, j)
                neig.h = heuristicFunction(i, j, iGoal, jGoal)
                neig.F = neig.g + neig.h * weight
                neig.k = k
                neig.parent = current
                if current.i == iStart and current.j == jStart:
                    neig.startingNodeEdgesMask = (1 << EDGES.index(e))
                else:
                    neig.startingNodeEdgesMask = current.startingNodeEdgesMask
                OPEN.AddNode(neig)
        k += 1

    return False, None, CLOSED, OPEN



# Реализация предпосчета Bounding Boxes на переданной карте

def GetStartingNodeEdgesMask(i, j, closed, gridMap):
    if not gridMap.Traversable(i, j):
        return 0
    ij = i, j
    try:
        ans = closed.elements[ij].startingNodeEdgesMask
    except Exception as e:
        print('AHTUNG')
        print(closed.elements.keys())
        raise e
    return ans


def PrecomputeBoundingBoxes(gridMap):
    # Initialize data
    bb = {}
    for i, row in enumerate(gridMap.cells):
        for j, cell in enumerate(row):
            for e in EDGES:
                bb[(i, j, e)] = {'r': {'min': MAX_INT, 'max': 0}, 'c': {'min': MAX_INT, 'max': 0}}

    # Calculate all Bounding Boxes
    for i, row_i in enumerate(gridMap.cells):
        for j, cell_j in enumerate(row_i):
            # Run 8bit-Dijkstra
            if not gridMap.Traversable(i, j):
                continue
            result = Dijkstra8bit(gridMap=gridMap, iStart=i, jStart=j, iGoal=-1, jGoal=-1)
            nodesExpanded = result[2]

            for p, row_p in enumerate(gridMap.cells):
                for q, cell_q in enumerate(row_p):
                    cur_edges = GetStartingNodeEdgesMask(p, q, nodesExpanded, gridMap)
                    for k, e in enumerate(EDGES):
                        if (cur_edges >> k) & 1:
                            bb[(i, j, e)]['r']['min'] = min(bb[(i, j, e)]['r']['min'], p)
                            bb[(i, j, e)]['r']['max'] = max(bb[(i, j, e)]['r']['max'], p)

                            bb[(i, j, e)]['c']['min'] = min(bb[(i, j, e)]['c']['min'], q)
                            bb[(i, j, e)]['c']['max'] = max(bb[(i, j, e)]['c']['max'], q)
    gridMap.bb = bb


