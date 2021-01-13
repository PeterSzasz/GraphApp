# generates a graph with nodes on random coordinates

from Core.graph import Graph, Node, Edge

from Utilities import randoms

class GraphGenerator:

    def __init__(self) -> None:
        self.random = randoms.RandomCoord()
        self.graph = Graph()

    def createNodes(self, nodeNum: int, width: int, height: int) -> None:
        self.random.setMaxX(width)
        self.random.setMaxY(height)
        for n in range(nodeNum):
            coord = self.random.generateCoord()
            self.graph.add_node(Node(coord[0], coord[1]))

    def createEdges(self, chance):
        self.random.setMax = 100
        for n1 in self.graph.nextNode():
            for n2 in self.graph.nextNode():
                if self.random.generate() < chance:
                    self.graph.add_edge(Edge(n1, n2))

    def genGraph(self, nodeNum: int, connection_chance: int, width: int, height: int) -> Graph:
        self.createNodes(nodeNum, width, height)
        self.createEdges(connection_chance)
        return self.graph
        