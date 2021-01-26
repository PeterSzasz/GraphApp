# generates a graph with nodes on random coordinates

import math
import random

from core.graph import Node, Edge, Graph
from graph_visualisation import VisGraph

from utilities.delaunay import Delaunay
from utilities.node_generator import RandomCoords, RandomRegionCoords


class GraphGenerator:

    def __init__(self) -> None:
        self.graph = VisGraph()
        self.random = None
        self.numberOfRegionsX = 7
        self.numberOfRegionsY = 8
        self.numberOfNodes = 5
        self.connection_chance = 2
        self.area_w = 640
        self.area_h = 480
        self.random = None
        self.nodeStrategyList = ['Whole Area Coords',
                                 'Region Coords',
                                 'Delaunay Coords'
                                ]
        self.nodeStrategy = 0
        self.edgeStrategyList = ['Random connections',
                                 'Delaunay triangulation'
                                ]
        self.edgeStrategy = 0
        
    def genGraph(self) -> Graph:
        self.graph.clearGraph()
        if self.nodeStrategy == 0:
            self.random = RandomCoords(self.numberOfNodes)
            self.createNodes(self.area_w, self.area_h)
        elif self.nodeStrategy == 1:
            self.random = RandomRegionCoords(self.numberOfNodes,
                                             self.numberOfRegionsX,
                                             self.numberOfRegionsY)
            self.createNodes(self.area_w, self.area_h)
        elif self.nodeStrategy == 2:
            pass

        if self.edgeStrategy == 0:
            self.createEdges_Random()
        elif self.edgeStrategy == 1:
            self.createEdges_Delaunay()

        return self.graph

    def createNodes(self, area_w: int, area_h: int) -> None:
        coords = self.random.generate((0,0),(area_w,area_h))
        for coord in coords:
            self.graph.addNode(Node(coord[0], coord[1]))

    def createEdges_Random(self):
        '''randomly creates connections based on chance'''
        for n1 in self.graph.nextNode():
            for n2 in self.graph.nextNode():
                if random.randint(0,100) < self.connection_chance:
                    edge = Edge(n1, n2)
                    self.graph.addEdge(edge)
                    n1.addEdge(edge)
                    n2.addEdge(edge)

    def createEdges_Delaunay(self):
        '''
        for every node we need the first and second closest
        with 3 point we can calculate the delaunay triangulation
        '''
        
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
            self.graph.addEdge(Edge(nodes,result[nodes][0]))
            self.graph.addEdge(Edge(nodes,result[nodes][1]))

    def genGraph_Delaunay(self) -> Graph:
        self.graph.clearGraph()
        self.createNodes(self.area_w, self.area_h)
        self.createEdges_Delaunay()
        return self.graph
        
if __name__ == "__main__":
    graph_gen = GraphGenerator()
