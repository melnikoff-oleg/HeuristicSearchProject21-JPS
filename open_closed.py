from node import Node

class OpenBase:

    def __init__(self):
        pass
    
    def __len__(self):
        pass
    
    def __iter__(self):
        pass

    def isEmpty(self):
        pass

    def AddNode(self, item : Node):
        pass

    def GetBestNode(self):
        pass


from heapq import heappop, heappush

class Open(OpenBase):
    def __init__(self):
        self.prioritizedQueue=[]
        self.ij_to_node={}
    
    def __iter__(self):
        return iter(self.ij_to_node.values())

    def __len__(self):
        return len(self.ij_to_node)
    
    def __str__(self):
        ans = ''
        for i in self.ij_to_node.keys():
            ans += str(i)
        return ans

    def isEmpty(self):
        return len(self.ij_to_node) == 0
        
    def AddNode(self, item : Node):
        ij = item.i, item.j
        oldNode = self.ij_to_node.get(ij)
        if oldNode is None or item.g <= oldNode.g:
            if not oldNode is None:
                item.startingNodeEdgesMask |= oldNode.startingNodeEdgesMask
            self.ij_to_node[ij] = item
            heappush(self.prioritizedQueue, item)

    def GetBestNode(self):
        bestNode = heappop(self.prioritizedQueue)
        ij = bestNode.i, bestNode.j
        while self.ij_to_node.pop(ij, None) is None:
            bestNode = heappop(self.prioritizedQueue)
            ij = bestNode.i, bestNode.j
        return bestNode





class ClosedBase:

    def __init__(self):
        pass

    def __iter__(self):
        pass
    
    def __len__(self):
        pass
    
    def AddNode(self, item : Node, *args):
        pass

    def WasExpanded(self, item : Node, *args):
        pass


class Closed(ClosedBase):
    
    def __init__(self):
        self.elements = {}

    def __iter__(self):
        return iter(self.elements.values())
    
    def __len__(self):
        return len(self.elements)
    
    def AddNode(self, item : Node):
        ij = item.i, item.j
        self.elements[ij] = item

    def WasExpanded(self, item : Node):
        ij = item.i, item.j
        return ij in self.elements.keys()



