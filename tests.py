from map import Map
from node import Node
from open_closed import Open, Closed
from distances import *
from consts import *
from BB_preprocessing import PrecomputeBoundingBoxes
from AStar import AStar



# ### Make Path
# This is an auxiliary function that reconstructs a path (i.e. the sequence on moves from start to goal) given a search tree, created by the search algorithm. It basically unwinds the path using the parent pointers. It also returns a length of the path.
def MakePath(goal):
    length = goal.g
    current = goal
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    path.append(current)
    return path[::-1], length



# ### Simple Single Test
# This function helps you to run a test of your search algorithm on a single instance (map + start + goal) and validate the result (provided that you know the correct answer to the path finding query and pass it as a parameter).



def SimpleTest(SearchFunction, height, width, mapstr, iStart, jStart, iGoal, jGoal, pathLen, **kwargs):
    taskMap = Map()
    taskMap.ReadFromString(mapstr, width, height)
    start = Node(iStart, jStart)
    goal = Node(iGoal, jGoal)

    try:
        result = SearchFunction(taskMap, start.i, start.j, goal.i, goal.j, **kwargs)
        nodesExpanded = result[2]
        nodesOpened = result[3]
        if result[0]:
            path = MakePath(result[1])
            correct = abs(path[1] - pathLen) < EPS
            print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
        else:
            print("Path not found!")
    except Exception as e:
        print("Execution error")
        print(e)
        # raise e

def SimpleTestBB(SearchFunction, height, width, mapstr, **kwargs):
    taskMap = Map()
    taskMap.ReadFromString(mapstr, width, height)

    try:
        PrecomputeBoundingBoxes(taskMap)
        for i in range(height - 5, height):
            for j in range(width - 5, width):
                if taskMap.Traversable(i, j):
                    print(i, j, taskMap.bb[(i, j, (0, 1))])
    except Exception as e:
        print("Execution error")
        # print(e)
        raise e


def SimpleTestAstarBB(SearchFunction, height, width, mapstr, iStart, jStart, iGoal, jGoal, pathLen, **kwargs):
    taskMap = Map()
    taskMap.ReadFromString(mapstr, width, height)
    PrecomputeBoundingBoxes(taskMap)
    start = Node(iStart, jStart)
    goal = Node(iGoal, jGoal)

    try:
        result = SearchFunction(taskMap, start.i, start.j, goal.i, goal.j, **kwargs)
        nodesExpanded = result[2]
        nodesOpened = result[3]
        if result[0]:
            path = MakePath(result[1])
            correct = abs(path[1] - pathLen) < EPS
            print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
        else:
            print("Path not found!")
    except Exception as e:
        print("Execution error")
        print(e)


def SimpleTestAstarBBNoPrep(SearchFunction, height, width, taskMap, iStart, jStart, iGoal, jGoal, pathLen, **kwargs):
    start = Node(iStart, jStart)
    goal = Node(iGoal, jGoal)

    try:
        result = SearchFunction(taskMap, start.i, start.j, goal.i, goal.j, **kwargs)
        nodesExpanded = result[2]
        nodesOpened = result[3]
        if result[0]:
            path = MakePath(result[1])
            correct = abs(path[1] - pathLen) < EPS
            print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
        else:
            print("Path not found!")
    except Exception as e:
        print("Execution error")
        print(e)


import random
random.seed = 35

def ReadTasksFromMovingAIFile(path):
    tasks = []
    with open(path + '_V2.map.scen') as taskFile:
        lines = taskFile.readlines()[1:]
    for i in lines:
        parts = i[:-1].split('	')
        tasks.append({'jStart': int(parts[-5]), 'iStart': int(parts[-4]), 'jGoal': int(parts[-3]),          'iGoal': int(parts[-2]), 'length': float(parts[-1])})
    
    return random.sample(tasks, 75)



# Все карты в movingai не предусматривают срезание углов, а наш алгоритм может срезать углы, когда срезается только одна клетка

# Поэтому мы написали специальную функцию, которая по тесту с movingai делает новый тест на основе А*, в котором посчитаны правильные длины путей, с учетом возможности срезать угол



def UpdateTasksFromMovingAIFile(filePath):

    mapName = filePath.split('/')[-1]

    taskMap = Map()
    taskMap.ReadFromFile('Data/' + mapName)

    with open(filePath + '.map.scen') as taskFile:
        lines = taskFile.readlines()

    lines = lines
    ans = []
    for i in lines[1:]:
        parts = i[:-1].split('	')
        task = {'jStart': int(parts[-5]), 'iStart': int(parts[-4]), 'jGoal': int(parts[-3]),          'iGoal': int(parts[-2]), 'length': float(parts[-1])}

        length = task['length']
        result = AStar(gridMap=taskMap, iStart=task['iStart'], jStart=task['jStart'], iGoal=task['iGoal'], jGoal=task['jGoal'])
        nodesExpanded = result[2]
        nodesOpened = result[3]
        if result[0]:
            path = MakePath(result[1]) 
            
            correct = abs(path[1] - length) < EPS
            
            print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
            ans.append(str(path[1]))
        else:
            print("Path not found!")
            
    
    with open(filePath + '_V2.map.scen', 'w') as taskFile:
        taskFile.write(lines[0])
        for i in range(1, len(lines)):
            new_line = '	'.join(lines[i].split('	')[:-1])
            taskFile.write(new_line + '	' + ans[i - 1] + '\n')

# UpdateTasksFromMovingAIFile('Data/arena')
# UpdateTasksFromMovingAIFile('Data/arena2')




# Massive Test


globalTasks = {}
for i in ['arena', 'arena2']: # 'arena2', 'brc000d', 'brc300d'
    globalTasks[i] = ReadTasksFromMovingAIFile('Data/' + i)

def MassiveTest(SearchFunction, mapsNames, **kwargs):
    stat = dict()
    stat["corr"] = []
    stat["len"] = []
    stat["nc"] = []
    stat["st"] = []
    for mapName in mapsNames:
        taskMap = Map()
        taskMap.ReadFromFile('Data/' + mapName)
        tasks = globalTasks[mapName]
        for task in tasks:
            try:
                length = task['length']
                result = SearchFunction(gridMap=taskMap, iStart=task['iStart'], jStart=task['jStart'], iGoal=task['iGoal'], jGoal=task['jGoal'], **kwargs)
                nodesExpanded = result[2]
                nodesOpened = result[3]
                if result[0]:
                    path = MakePath(result[1]) 
                    stat["len"].append(path[1])
                    correct = abs(path[1] - length) < EPS
                    stat["corr"].append(correct)
                    print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
                else:
                    print("Path not found!")
                    stat["corr"].append(False)
                    stat["len"].append(0.0)

                stat["nc"].append(len(nodesOpened) + len(nodesExpanded))
                stat["st"].append(len(nodesExpanded))

            except Exception as e:
                print("Execution error")
                print(e)

    return stat


import time


def MassiveTestBB(SearchFunction, mapsNames, **kwargs):
    stat = dict()
    stat["corr"] = []
    stat["len"] = []
    stat["nc"] = []
    stat["st"] = []
    for mapName in mapsNames:
        taskMap = Map()
        taskMap.ReadFromFile('Data/' + mapName)
        print('Map', mapName, 'BB Preprocessing')
        start_time = time.time()
        PrecomputeBoundingBoxes(taskMap)
        print("--- %s seconds ---" % (time.time() - start_time))
        print('Map', mapName, 'BB Preprocessing Finished')
        tasks = globalTasks[mapName]
        for task in tasks:
            try:
                length = task['length']
                result = SearchFunction(gridMap=taskMap, iStart=task['iStart'], jStart=task['jStart'], iGoal=task['iGoal'], jGoal=task['jGoal'], **kwargs)
                nodesExpanded = result[2]
                nodesOpened = result[3]
                if result[0]:
                    path = MakePath(result[1]) 
                    stat["len"].append(path[1])
                    correct = abs(path[1] - length) < EPS
                    stat["corr"].append(correct)
                    print("Path found! Length: " + str(path[1]) + ". Nodes created: " + str(len(nodesOpened) + len(nodesExpanded)) + ". Number of steps: " + str(len(nodesExpanded)) + ". Correct: " + str(correct))
                else:
                    print("Path not found!")
                    stat["corr"].append(False)
                    stat["len"].append(0.0)

                stat["nc"].append(len(nodesOpened) + len(nodesExpanded))
                stat["st"].append(len(nodesExpanded))

            except Exception as e:
                print("Execution error")
                print(e)

    return stat


