# inherited from Graph class, extends the base class with

from core.graph import Graph


class VisGraph(Graph):
    '''Simple graph class extended with option to mark edges and nodes as highlighted.'''

    def __init__(self):
        super().__init__()
        self.highlighted_edge = []
        self.highlighted_node = []

    def highlightEdgeSwitch(self, edge):
        '''Turns edge(Edge) highlight on/off.'''
        if edge in self.highlighted_edge:
            self.highlighted_edge.remove(edge)
        else:
            self.highlighted_edge.append(edge)

    def highlightNodeSwitch(self, node):
        '''Turns node(Node) highlight on/off.'''
        if node in self.highlighted_node:
            self.highlighted_node.remove(node)
        else:
            self.highlighted_node.append(node)

    def nextHighlightedNode(self):
        '''generator method, traverse through already highlighted nodes'''
        for node in self.highlighted_node:
            yield node

    def nextHighlightedEdge(self):
        '''generator method, traverse through already highlighted edges'''
        for edge in self.highlighted_edge:
            yield edge