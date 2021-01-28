# simple, common graph, mainly for inheritance

import random

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
        self.nodes = []
        self.edges = []
        self.incidence_m = [] #TODO: list?
        self.nodes_hash_seed = random.randint(0, 9999999)
        self.edges_hash_seed = random.randint(0, 9999999)

    def __hash__(self) -> int:
        node_avg = 0
        edge_avg = 0
        nodes_hash = self.nodes_hash_seed
        edges_hash = self.edges_hash_seed
        for node in self.nextNode():
            nodes_hash += hash(node)
        for edge in self.nextEdge():
            edges_hash += hash(edge)
        if len(self.nodes) != 0:
            node_avg = self.nodes_hash / len(self.nodes)
        if len(self.edges) != 0:
            edge_avg = self.edges_hash / len(self.edges)
        return int((node_avg + edge_avg)/2)
        
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
        self.nodes_hash = random.randint(0, 999999)
        self.edges_hash = random.randint(0, 999999)

    class InvalidVertexError(Exception):
        def __init__(self, message):
            self.message = message


if __name__ == "__main__":
    graph = Graph()