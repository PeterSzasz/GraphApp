# generates a graph with nodes on random coordinates

import math
import random

from core.graph import Node, Edge, Graph
from graph_visualisation import VisGraph

from utilities.delaunay import Delaunay
from utilities.node_generator import RandomCoords, RandomRegionCoords


class GraphGenerator:
    '''
    Sets and stores different graph generator methods (strategies).
    Calls appropriate in genGraph. Simpler calculations (like two-closest-node)
    are developed here, others are called from different classes (Delaunay).
    '''
    def __init__(self) -> None:
        self.graph = VisGraph()
        self.random = None
        self.numberOfRegionsX = 7
        self.numberOfRegionsY = 7
        self.numberOfNodes = 15
        self.connection_chance = 2
        self.area_w = 640
        self.area_h = 480
        self.random = None
        self.nodeStrategyList = ['Whole Area Coords',
                                 'Region Coords',
                                 'Delaunay Coords'
                                ]
        self.nodeStrategy = 1
        self.edgeStrategyList = ['Random connections',
                                 'Two Closest nodes',
                                 'Delaunay triangulation'
                                ]
        self.edgeStrategy = 2
        
    def genGraph(self) -> Graph:
        '''Initiates a graph node and graph edge generator methods.
            Edge and node strategy set separately, eg.: in gui class'''
        self.graph.clearGraph()
        if self.nodeStrategy == 0:
            self.random = RandomCoords(self.numberOfNodes)
            self.createNodes_Random(self.area_w, self.area_h)
        elif self.nodeStrategy == 1:
            self.random = RandomRegionCoords(self.numberOfNodes,
                                             self.numberOfRegionsX,
                                             self.numberOfRegionsY)
            self.createNodes_Random(self.area_w, self.area_h)
        elif self.nodeStrategy == 2:
            pass

        if self.edgeStrategy == 0:
            self.createEdges_Random()
        elif self.edgeStrategy == 1:
            self.createEdges_ClosestTwo()
        elif self.edgeStrategy == 2:
            self.createEdges_Delaunay()

        return self.graph

    def createNodes_Random(self, area_w: int, area_h: int) -> None:
        '''creates nodes on random coordinates'''
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

    def createEdges_ClosestTwo(self) -> None:
        '''
        for every node we calculates the first and second closest
        then creates and adds the edges to the graph and to the nodes
        '''
        
        result = {}
        first = None,math.inf
        second = None,math.inf
        for n1 in self.graph.nextNode():            # calculates the two closest node
            for n2 in self.graph.nextNode():        # for each node, TODO: optimise calc
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

        for node_from in result:                    # sets the neighbours for each node
            first_closest = result[node_from][0]
            second_closest = result[node_from][1]
            first_edge = Edge(node_from,first_closest)
            self.graph.addEdge(first_edge)
            node_from.addEdge(first_edge)
            first_closest.addEdge(first_edge)
            second_edge = Edge(node_from,second_closest)
            self.graph.addEdge(second_edge)
            node_from.addEdge(second_edge)
            second_closest.addEdge(second_edge)

    def createEdges_Delaunay(self):
        '''
        with 3 point we can calculate the delaunay triangulation
        '''
        delaunay = Delaunay()
        new_edges = delaunay.generate(self.graph.nodes)
        if new_edges:
            self.graph.edges = new_edges
            
if __name__ == "__main__":
    graph_gen = GraphGenerator()
