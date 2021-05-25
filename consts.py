import math

EPS = 0.01
MAX_INT = 1e18
EDGES = ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
SQRT2 = math.sqrt(2)


# Computes a cost of transition from cell (i1, j1) to cell (i2, j2)
def ComputeCost(i1, j1, i2, j2):
    md = abs(i1 - i2) + abs(j1 - j2)
    if md == 2:
        return SQRT2
    else:
        return md

        