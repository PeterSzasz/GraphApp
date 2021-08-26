# delaunay triangulation

from math import sqrt
import numpy as np
from utilities.node_generator import NodeGeneratorBase
from core.graph import Node,Edge, Graph

class Triangle(Graph):
    '''
    helper class for delaunay triangulation
    the Bowyer-Watson algorithm uses it mostly
    '''
    def __init__(self):
        super().__init__()
        self.addNode(Node(0,0))
        self.addNode(Node(0,0))
        self.addNode(Node(0,0))

    def __str__(self):
        return str(f"<A:{self.getA()} B:{self.getB()} C: {self.getC()}>")

    def addNode(self, node: Node):
        if len(self.nodes) == 3:
            self.setC(self.nodes[1])
            self.setB(self.nodes[0])
            self.setA(node)
        else:
            super().addNode(node)

    def setA(self, node: Node):
        self.nodes[0] = node
    def setB(self, node: Node):
        self.nodes[1] = node
    def setC(self, node: Node):
        self.nodes[2] = node

    def getA(self) -> Node:
        return self.nodes[0]
    def getB(self) -> Node:
        return self.nodes[1]
    def getC(self) -> Node:
        return self.nodes[2]

    def checkNode(self, node):
        if node == self.getA() or \
            node == self.getB() or \
            node == self.getC():
            return True
        else:
            return False

    def getAB(self) -> Edge:
        return Edge(self.getA(),self.getB())
    def getBC(self) -> Edge:
        return Edge(self.getB(),self.getC())
    def getCA(self) -> Edge:
        return Edge(self.getC(),self.getA())

    def nextEdge(self) -> Edge:
        yield self.getAB()
        yield self.getBC()
        yield self.getCA()
    
    def checkEdge(self, edge) -> bool:
        if edge == self.getAB() or \
            edge == self.getBC() or \
            edge == self.getCA():
            return True
        else:
            return False

class Delaunay(NodeGeneratorBase):
    '''
    Class for generating the Delaunay triangluation on given coordinates.
    https://en.wikipedia.org/wiki/Delaunay_triangulation
    '''

    def __init__(self) -> None:
        super().__init__()

    def generate(self, nodes: list[Node]) -> tuple[list[Edge],list[Edge]]:
        '''        
        Bowyer-Watson algorithm
        https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm

        Args:
            nodes (list[Node]): list of individual points that the
                                delaunay triangulation should run on

        Returns:
            list[Edge]: list of edges (point pairs) that 
        '''
        
        delaunay_result: list[Edge] = []
        voronoi_result: list[Edge] = []
        voronoi_data = {}
        if not nodes:
            return delaunay_result, voronoi_result
        triangulation: list[Triangle] = []
        super_triangle = Triangle()
        # TODO: should calculate min-max points and set accordingly
        super_triangle.setA(Node(500,10000))
        super_triangle.setB(Node(10000,-10000))
        super_triangle.setC(Node(-10000,-10000))
        triangulation.append(super_triangle)

        for node in nodes:
            bad_triangles = []
            for tri in triangulation:
                A = (tri.getA().x(),tri.getA().y())
                B = (tri.getB().x(),tri.getB().y())
                C = (tri.getC().x(),tri.getC().y())
                # get circumcircle center and radius
                cc_x, cc_y, cc_r = self.calcCircleMidpoint(A,B,C)
                diff_x = cc_x - node.x()
                diff_y = cc_y - node.y()
                diff_length = sqrt(diff_x*diff_x + diff_y*diff_y)
                if diff_length < cc_r:
                    # new point is within circumcircle
                    bad_triangles.append(tri)
                # TODO: should store cc center for Voronoi
                vor_node = Node(int(cc_x),int(cc_y))
                vor_node.data = {"center_node": node}
                voronoi_data[tri] = vor_node
            polygon = []
            for tri1 in bad_triangles:
                # find bounding edges of polygonal hole
                # around new point
                for edge in tri1.nextEdge():
                    shared = False
                    for tri2 in bad_triangles:
                        if tri1 == tri2:
                            continue
                        if tri2.checkEdge(edge):
                            shared = True
                    if not shared:
                        polygon.append(edge)
            for tri in bad_triangles:
                # remove invalidated triangles
                triangulation.remove(tri)
            for edge in polygon:
                # re-triangulate the polygonal hole
                newTri = Triangle()
                newTri.setA(edge.n1())
                newTri.setB(edge.n2())
                newTri.setC(node)
                triangulation.append(newTri)
        for tri in triangulation:
            # create return edge package, 
            # except edges connected to big helper triangle
            if tri.checkNode(super_triangle.getA()) or \
                tri.checkNode(super_triangle.getB()) or \
                tri.checkNode(super_triangle.getC()):
                continue
            delaunay_result.append(tri.getAB())
            delaunay_result.append(tri.getBC())
            delaunay_result.append(tri.getCA())
            # create voronoi
            A = (tri.getA().x(),tri.getA().y())
            B = (tri.getB().x(),tri.getB().y())
            C = (tri.getC().x(),tri.getC().y())
            # get circumcircle center and radius
            cc_x, cc_y, cc_r = self.calcCircleMidpoint(A,B,C)
            voronoi_node = Node(int(cc_x),int(cc_y))
            voronoi_node.data = {"sites":{tri.getA(),tri.getB(),tri.getC()}}
            voronoi_result.append(voronoi_node)

        voronoi_result = list(set(voronoi_result))
        delaunay_result = list(set(delaunay_result))
        return delaunay_result, voronoi_result

    def generate_circlecheck(self, nodes: list[Node]) -> list[Edge]:
        # a brute force version
        # generate edges:
        # iterate through list of nodes and generates the circles (midpoints)
        # checks if there are any other node inside the circle
        # if not the circle is valid and the nodes should be connected
        # generate nodes:
        # iterate through list of nodes and generates the circles
        # ...
        pass

    def calcCircleMidpoint(self, point1: tuple, point2: tuple, point3: tuple) -> tuple:
        '''
        Gives the midpoint and radius of a circle that passing through 3 points.
        - first calculates two midpoints (M1,M2), 
        - then with the bisector lines' equations on these points
            - L1 line perpendicular to P2-P1 line and intersects M1:
                L1 = M1 + T[0] * V1
            - L2 line perpendicular to P3-P1 line and intersects M2:
                L2 = M2 + T[1] * V2
        - it calculates the intersection of these lines which give us a variable (T)
        - inserting this (T) variable in one of the line equations
          it gives the circle's midpoint

        Args:
            point1 ([type]): first point on circle's circumference
            point2 ([type]): second point on circle's circumference
            point3 ([type]): third point on circle's circumference
        Return:
            circle's midpoint x, y and radius
        '''
        
        # rotation matrix
        theta = np.radians(90)
        rot = np.array([(np.cos(theta), -np.sin(theta)),(np.sin(theta), np.cos(theta))])
        P1 = np.array(point1)
        P2 = np.array(point2)
        P3 = np.array(point3)
        # M1 midpoint between P2 and P1
        M1 = P1 + (P2 - P1)/2
        # V1 
        V1 = ((P2 - P1) @ rot)

        # M2 midpoint between P3 and P1
        M2 = P1 + (P3 - P1)/2
        # V2
        V2 = ((P3 - P1) @ rot)
        
        # solve(L1 = L2) -> midpointC
        T = np.linalg.solve(np.array([(V1[0],-V2[0]),(V1[1],-V2[1])]), 
                            np.array([(M2[0]-M1[0]),(M2[1]-M1[1])]))
        
        # with T this gives us the intersection point of L1 and L2
        L2 = M2 + T[1] * V2
        
        # circles radius
        radius = np.linalg.norm([L2-P1])
        
        return L2[0],L2[1],radius

if __name__ == "__main__":
    triang = Delaunay()
    res = triang.calcCircleMidpoint((1,2), (4,2), (2,4))
    print(f"circumcircle method: {res}")
    res = triang.generate([Node(1,2),Node(2,2),Node(5,5),Node(4,8)])
    print(f"delaunay edges: {res}")
    
    tri = Triangle()
    print(tri)
    tri.addNode(Node(1,1))
    print(tri)
    tri.addNode(Node(2,2))
    print(tri)
    tri.addNode(Node(3,2))
    print(tri)
    tri.addNode(Node(4,2))
    print(tri)
    tri.setB(Node(5,1))
    print(tri)