# Qt5 Widget for drawing graphs

import math
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QMouseEvent, QPainter, QPaintEvent, QPalette, QPen, QStaticText
from PyQt5.QtWidgets import QWidget

from core.graph import Edge, Graph, Node


class GraphRender(QWidget):
    '''an area that can be used for drawing graphs, used within a Qt window/widget'''

    def __init__(self) -> None:
        super().__init__()
        self.graph = None
        self.area_w = 1024
        self.area_h = 768
        self.setMinimumSize(self.area_w, self.area_h)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.image = QImage(self.area_w, self.area_h, QImage.Format_ARGB32)

    def setGraph(self, graph: Graph):
        self.graph = graph

    def voronoiBackground(self, posX: int, posY: int) -> int:
        closest = self.area_h * self.area_w
        for node in self.graph.nextNode():
            diff = (abs(posX - node.x()), abs(posY - node.y()))
            diff_length = math.sqrt(diff[0]**2 + diff[1]**2)
            if diff_length < closest:
                closest = diff_length
        return math.floor(closest)

    def drawBackground(self):
        # voronoi pixelate, kindof
        pixel_size = 8
        painter = QPainter(self.image)
        #painter.setRenderHint(QPainter.Antialiasing)
        start_time = time.perf_counter()
        if self.graph.nodes:
            for x in range(0, self.area_w, pixel_size):
                for y in range(0, self.area_h, pixel_size):
                    dist = self.voronoiBackground(x, y)
                    dist = 255 - dist
                    if dist < 0: dist = 0
                    painter.setPen(QPen(QColor(dist, dist, dist, 255), pixel_size))
                    painter.drawPoint(x, y)
        stop_time = time.perf_counter()
        print(stop_time - start_time)
        #painter.setRenderHint(QPainter.Antialiasing, False)
        painter.end()

    def drawEdges(self):
        # draw the edges
        node_width = 8
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.white, node_width//2))
        painter.drawRect(0, 0, self.area_w, self.area_h)
        painter.setPen(QPen(Qt.darkGray, node_width//2))
        for edge in self.graph.nextEdge():
            painter.drawLine(edge.n1().x(),
                             edge.n1().y(),
                             edge.n2().x(),
                             edge.n2().y())
        painter.end()

    def drawNodes(self):
        # draw the nodes
        node_width = 8
        painter = QPainter(self.image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, node_width//2))
        for node in self.graph.nextNode():
            painter.drawEllipse(node.x() - node_width//2,
                                node.y() - node_width//2,
                                node_width,
                                node_width)
            painter.drawStaticText(node.x() - 30, node.y() + 5, QStaticText(str(node)))
        painter.end()

    def paintEvent(self, a0: QPaintEvent) -> None:
        self.drawBackground()
        self.drawNodes()
        self.drawEdges()
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        painter.end()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(a0.localPos())
        for node in self.graph.nextNode():
            if abs(node.x() - a0.localPos().x()) < 20 and abs(node.y() - a0.localPos().y()) < 20:
                print(node)
        return super().mousePressEvent(a0)