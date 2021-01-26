# delaunay triangulation

import numpy as np
from utilities.node_generator import NodeGeneratorBase

class Delaunay(NodeGeneratorBase):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> list:
        # generate edges:
        # iterate through list of nodes and generates the circles
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
    result = triang.calcCircleMidpoint((1,2), (4,2), (2,4))
    print(result)