import math

def DiagonalDistance(i1, j1, i2, j2):
    x = abs(i1 - i2)
    y = abs(j1 - j2)
    return min(x, y) + abs(x - y)

def ChebyshevDistance(i1, j1, i2, j2):
    x = abs(i1 - i2)
    y = abs(j1 - j2)
    return max(x, y)

def EuclidDistance(i1, j1, i2, j2):
    return math.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)

    