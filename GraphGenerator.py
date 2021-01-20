# generates a graph with nodes on random coordinates

import random
from Core.graph import Graph, Node, Edge

from Utilities import randoms

class GraphGenerator:

    def __init__(self) -> None:
        self.graph = Graph()
        self.random = randoms.RandomBase()

    def setRandomStrategy(self, randomClass: randoms.RandomBase):
        self.random = randomClass

    def createNodes(self, area_w: int, area_h: int) -> None:
        coords = self.random.generate((0,0),(area_w,area_h))
        for coord in coords:
            self.graph.add_node(Node(coord[0], coord[1]))

    def createEdges(self, chance):
        for n1 in self.graph.nextNode():
            for n2 in self.graph.nextNode():
                # TODO: dirty method to connect nodes, should replace (w delaunay)
                if random.randint(0,100) < chance:
                    self.graph.add_edge(Edge(n1, n2))

    def genGraph(self, connection_chance: int, area_w: int, area_h: int) -> Graph:
        self.graph.clearGraph()
        self.createNodes(area_w, area_h)
        self.createEdges(connection_chance)
        return self.graph
        