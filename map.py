from consts import *



# Реализация класса для хранения карты. В нем же реализованы методы сокращения succesor-ов, по методу JPS.

# Тут важный момент что в нашей карте допускается срезания угла при диагональном ходе, если срезается только один угол, а не два.

class Map:

    # Default constructor
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []
        self.bb = {}
    
    # Initialization of map by string.
    def ReadFromString(self, cellStr, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cellLines = cellStr.split("\n")
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == 'T' or c == '#' or c == '@':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                # TODO
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width )
                
                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height )

    # Initialization from moving ai file
    def ReadFromFile(self, path, traversable=['.', 'G'], blocked=['T', '@', 'O']):
        with open(path + '.map') as file:
            lines = file.readlines()
        self.height = int(lines[1].split(' ')[-1][:-1])
        self.width = int(lines[2].split(' ')[-1][:-1])
        self.cells = [[0 for _ in range(self.width)] for _ in range(self.height)]
        cellLines = [line[:-1] for line in lines[4:]]
        i = 0
        j = 0
        for l in cellLines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c in traversable:
                        self.cells[i][j] = 0
                    elif c in blocked:
                        self.cells[i][j] = 1
                    else:
                        raise Exception("Unknown cell type: ", j)
                    j += 1

                if j != self.width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width )
                
                i += 1

        if i != self.height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height )

        # img = mpimg.imread(path + '.png')
        # plt.imshow(img)
        # plt.show()
    

    # Checks cell is on grid.
    def inBounds(self, i, j):
        return (0 <= j < self.width) and (0 <= i < self.height)
    
    # Checks cell is not obstacle.
    def Traversable(self, i, j):
        return not self.cells[i][j]

    # Creates a list of neighbour cells as (i,j) tuples.
    def GetNeighborsOld(self, i, j):
        neighbors = []
        delta_h_v = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        delta_d = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

        for d in delta_h_v:
            if self.inBounds(i + d[0], j + d[1]) and self.Traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        
        for d in delta_d:
            if self.inBounds(i + d[0], j + d[1]) and self.Traversable(i + d[0], j + d[1]) and self.Traversable(i + d[0], j) and self.Traversable(i, j + d[1]):
                neighbors.append((i + d[0], j + d[1]))

        return neighbors


    # Checks if a move in the given direction can be made
    def canMove(self, i, j, di, dj):
        md = abs(di) + abs(dj)
        if md == 1:
            return self.inBounds(i + di, j + dj) and self.Traversable(i + di, j + dj)
        if md == 2:
            return (self.inBounds(i + di, j + dj) and 
                    self.Traversable(i + di, j + dj) and 
                    (self.Traversable(i + di, j) or
                    self.Traversable(i, j + dj)))
        return False


    # Creates a list of neighbour cells as (i,j) tuples.
    def GetNeighbors(self, i, j):
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if self.canMove(i, j, di, dj):
                    neighbors.append((i + di, j + dj))

        return neighbors

    # Prune neighbours of (i2, j2) for JPS algorithm; (i1, j1) is the parent
    def GetPrunedNeighbors(self, i1, j1, i2, j2, indicateForcedNeighbors=False):
        di = i2 - i1
        dj = j2 - j1
        succ = []
        # Natural neighbour in the same direction
        if self.canMove(i2, j2, di, dj):
            succ.append((i2 + di, j2 + dj))

        hasForcedNeighbors = False
        # Diagonal move
        if ComputeCost(i1, j1, i2, j2) > 1:
            # Natural neighbours
            if self.canMove(i2, j2, 0, dj):
                succ.append((i2, j2 + dj))
            if self.canMove(i2, j2, di, 0):
                succ.append((i2 + di, j2))
            # Forced neighbours
            if not self.Traversable(i1, j2) and self.canMove(i2, j2, -di, dj):
                succ.append((i1, j2 + dj))
                hasForcedNeighbors = True
            if not self.Traversable(i2, j1) and self.canMove(i2, j2, di, -dj):
                succ.append((i2 + di, j1))
                hasForcedNeighbors = True
        # Straight move
        else:
        # Only forced neighbours in this case
            if di == 0:
                for move_i in (-1, 1):
                    if self.inBounds(i2 + move_i, j2) and (not self.Traversable(i2 + move_i, j2)) and self.canMove(i2, j2, move_i, dj):
                        succ.append((i2 + move_i, j2 + dj))
                        hasForcedNeighbors = True
            else:
                for move_j in (-1, 1):
                    if self.inBounds(i2, j2 + move_j) and (not self.Traversable(i2, j2 + move_j)) and self.canMove(i2, j2, di, move_j):
                        succ.append((i2 + di, j2 + move_j))
                        hasForcedNeighbors = True

        if indicateForcedNeighbors:
            return succ, hasForcedNeighbors

        return succ

    def GetSuccessors(self, node, goal, limit=-1):
        i, j = node.i, node.j
        neighbours = []
        successors = []
        parent = node.parent
        if parent is not None:
            neighbours = self.GetPrunedNeighbors(parent.i, parent.j, i, j)
        else:
            neighbours = self.GetNeighbors(i, j)
        for ni, nj in neighbours:
            next = self.jump(i, j, ni -i, nj - j, goal, limit)
            if next is not None:
                successors.append((next.i, next.j))
        
        return successors
    
    def jump(self, i, j, di, dj, goal, limit=-1):

        if not self.canMove(i, j, di, dj):
            return None
        ni = i + di
        nj = j + dj
        n = Node(ni, nj)
        if limit == 0 or n == goal:
            return n
        
        if limit > -1:
            limit -= 1
        _, hasForced = self.GetPrunedNeighbors(i, j, ni, nj, indicateForcedNeighbors=True)
        if hasForced:
            return n
        
        if abs(di) + abs(dj) == 2:
            if (self.jump(ni, nj, 0, dj, goal, limit) is not None or
                self.jump(ni, nj, di, 0, goal, limit) is not None):
                return n
        return self.jump(ni, nj, di, dj, goal, limit)



