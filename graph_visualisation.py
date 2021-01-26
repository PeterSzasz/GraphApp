# inherited from Graph class, extends the base class with

from core.graph import Graph


class VisGraph(Graph):

    def __init__(self):
        super().__init__()
        self.highlighted_edge = []
        self.highlighted_node = []

    def highlightEdgeSwitch(self, edge):
        if edge in self.highlighted_edge:
            self.highlighted_edge.remove(edge)
        else:
            self.highlighted_edge.append(edge)

    def highlightNodeSwitch(self, node):
        if node in self.highlighted_node:
            self.highlighted_node.remove(node)
        else:
            self.highlighted_node.append(node)

    def nextHighlightedNode(self):
        for node in self.highlighted_node:
            yield node

    def nextHighlightedEdge(self):
        for edge in self.highlighted_edge:
            yield edge