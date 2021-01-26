# simple, common graph, mainly for inheritance

class Node:
    '''graph node with position'''

    def __init__(self, posx, posy):
        self.posX = posx
        self.posY = posy
        self.data = None
        self.edges = []

    def __str__(self) -> str:
        return "(" + str(self.posX) + "," + str(self.posY) + ")"

    def x(self):
        return self.posX

    def y(self):
        return self.posY

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def nextEdge(self):
        for edge in self.edges:
            yield edge

    def addData(self, data):
        self.data = data

    def getData(self):
        return self.data


class Edge:
    '''edge with two nodes'''

    def __init__(self, n1: Node, n2: Node):
        self.node1 = n1
        self.node2 = n2

    def __str__(self) -> str:
        return str(self.node1) + " -> " + str(self.node2)

    def n1(self):
        return self.node1

    def n2(self):
        return self.node2


class Graph:
    '''simple graph'''

    def __init__(self) -> None:
        self.edges = []
        self.nodes = []
        self.incidence_m = [] #TODO: list? realy?

    def addNode(self, node: Node):
        self.nodes.append(node)

    def addEdge(self, edge: Edge):
        if self.nodes.count(edge.n1()) == 0 or self.nodes.count(edge.n2()) == 0:
            raise self.InvalidVertexError("add_edge failed, start or end node missing")
        else:
            self.edges.append(edge)

    def nextNode(self):
        '''node generator'''
        for node in self.nodes:
            yield node

    def nextEdge(self):
        '''edge generator'''
        for edge in self.edges:
            yield edge

    def clearGraph(self):
        '''deletes all the nodes and edges'''
        self.edges.clear()
        self.nodes.clear()

    class InvalidVertexError(Exception):
        def __init__(self, message):
            self.message = message


if __name__ == "__main__":
    graph = Graph()