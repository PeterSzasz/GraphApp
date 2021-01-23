# generates a graph with nodes on random coordinates

import math
import random

from core.graph import Graph, Node, Edge

from utilities.delaunay import Triangulation
from utilities.node_generator import NodeGeneratorBase


class GraphGenerator:

    def __init__(self) -> None:
        self.graph = Graph()
        self.random = None

    def setNodesStrategy(self, randomClass):
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

    def createEdges_Delaunay(self):
        # for every node we need the first and second closest
        # with 3 point we can calculate the delaunay triangulation
        result = {}
        first = None,math.inf
        second = None,math.inf
        for n1 in self.graph.nextNode():
            print(str(n1))
            for n2 in self.graph.nextNode():
                if n2 == n1:
                    continue
                diff = (abs(n1.x() - n2.x()), abs(n1.y() - n2.y()))
                diff_length = math.sqrt(diff[0]**2 + diff[1]**2)
                if diff_length < first[1]:
                    first = n2,diff_length
                elif diff_length < second[1]:
                    second = n2,diff_length
            result[n1] = [first[0], second[0]]
            first = None,math.inf
            second = None,math.inf

        print("Nodes and neighbours:")
        for nodes in result:
            print(str(nodes), end=":\t")
            print(str(result[nodes][0]), end="\t")
            print(str(result[nodes][1]))
            self.graph.add_edge(Edge(nodes,result[nodes][0]))
            self.graph.add_edge(Edge(nodes,result[nodes][1]))
        

    def genGraph(self, connection_chance: int, area_w: int, area_h: int) -> Graph:
        self.graph.clearGraph()
        self.createNodes(area_w, area_h)
        self.createEdges(connection_chance)
        return self.graph

    def genGraph_Delaunay(self, area_w: int, area_h: int) -> Graph:
        self.graph.clearGraph()
        self.createNodes(area_w, area_h)
        self.createEdges_Delaunay()
        return self.graph
        
if __name__ == "__main__":
    rand = NodeGeneratorBase.RandomCoords(10)
    gg = GraphGenerator()
    gg.setNodesStrategy(rand)
    gg.genGraph_Delaunay(1024,768)
