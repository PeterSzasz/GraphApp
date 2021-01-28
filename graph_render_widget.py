# Qt5 Widget for drawing graphs

import math
import time
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QImage, QMouseEvent, QPainter, QPaintEvent, QPalette, QPen, QStaticText
from PyQt5.QtWidgets import QWidget
#import concurrent.futures
import multiprocessing

from graph_visualisation import VisGraph


class VoronoiBackground(QObject):
    finished = pyqtSignal()

    def __init__(self, graph: VisGraph, area_w: int, area_h: int, pixel_size: int, worker_image: QImage) -> None:
        super().__init__()
        self.graph = graph
        self.area_w = area_w
        self.area_h = area_h
        self.pixel_size = pixel_size
        self.bkg_image = worker_image

    def voronoiBackground(self, posX: int, posY: int) -> int:
        closest = math.inf
        for node in self.graph.nextNode():
            diff = (abs(posX - node.x()), abs(posY - node.y()))
            diff_length = math.sqrt(diff[0]**2 + diff[1]**2)
            if diff_length < closest:
                closest = diff_length
        return math.floor(closest)

    def run(self) -> QImage:
        print("Voronoi background method started.")
        
        painter = QPainter(self.bkg_image)
        start_time = time.perf_counter()
        if self.graph.nodes:
            for x in range(0, self.area_w, self.pixel_size):
                for y in range(0, self.area_h, self.pixel_size):
                    dist = self.voronoiBackground(x, y)
                    dist = 255 - dist
                    if dist < 0: dist = 0
                    painter.setPen(QPen(QColor(dist, dist, dist, 255), self.pixel_size))
                    painter.drawPoint(x, y)
        stop_time = time.perf_counter()
        print(stop_time - start_time)
        painter.end()
        self.finished.emit()
        

class GraphRender(QWidget):
    '''
    Represents an area that can be used for drawing graphs, 
    used within a Qt window/widget.
    '''

    def __init__(self) -> None:
        super().__init__()
        self.graph = None
        self.area_w = 1024
        self.area_h = 768
        self.pixel_size = 16
        self.setMinimumSize(self.area_w, self.area_h)
        self.graph_image = QImage(self.area_w, self.area_h, QImage.Format_ARGB32)
        self.bkg_image = QImage(self.area_w, self.area_h, QImage.Format_ARGB32)
        self.previous_hash = 0

    def setGraph(self, graph: VisGraph):
        '''sets a new graph reference and initiates a rendering of it'''
        self.graph = graph
        self.drawNodes()
        self.drawEdges()
        self.repaint()
        self.previous_hash = hash(self.graph)

    def drawBackground(self):
        '''calculates the background voronoi image in a separate thread'''
        self.worker_image = QImage(self.area_w, self.area_h, QImage.Format_ARGB32)
        self.work_thread = QThread()
        self.worker = VoronoiBackground(self.graph,
                                            self.area_w,
                                            self.area_h,
                                            self.pixel_size,
                                            self.worker_image)
        self.worker.moveToThread(self.work_thread)
        self.work_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.work_thread.quit)
        self.worker.finished.connect(self.work_thread.deleteLater)
        self.worker.finished.connect(self.worker.deleteLater)
        def finish():
            self.bkg_image = self.worker_image
            self.repaint()
        self.work_thread.finished.connect(finish)
        self.work_thread.start()

    def drawEdges(self, target = None):
        '''draws the graph edges'''
        if target:
            painter = QPainter(target)
        else:
            painter = QPainter(self.graph_image)
        node_width = 8
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.darkGray, node_width//2))
        for edge in self.graph.nextEdge():
            painter.drawLine(edge.n1().x(),
                             edge.n1().y(),
                             edge.n2().x(),
                             edge.n2().y())
        painter.end()

    def drawNodes(self, target = None):
        '''draws the graph nodes and prints its coords'''
        if target:
            painter = QPainter(target)
        else:
            painter = QPainter(self.graph_image)
        node_width = 8
        #painter.setRenderHint(QPainter.Antialiasing)
        for node in self.graph.nextNode():
            if node in self.graph.highlighted_node:
                painter.setPen(QPen(Qt.darkGreen, node_width//2))
            else:
                painter.setPen(QPen(Qt.black, node_width//2))
            painter.drawEllipse(node.x() - node_width//2,
                                node.y() - node_width//2,
                                node_width,
                                node_width)
            painter.setPen(QPen(Qt.black, node_width//2))
            painter.drawStaticText(node.x() - 30, node.y() + 5, QStaticText(str(node)))
        painter.end()

    def paintEvent(self, a0: QPaintEvent) -> None:
        # if the graph changed: clear
        if self.previous_hash != hash(self.graph):
            self.graph_image.fill(QColor(255,255,255,0))
            self.bkg_image.fill(QColor(255,255,255,0))
            self.previous_hash = hash(self.graph)
        # and repaint
        self.drawNodes()
        self.drawEdges()
        print(self.previous_hash)
        # combine the occasional background and the actual graph
        painter = QPainter(self.bkg_image)
        painter.drawImage(0, 0, self.graph_image)
        painter.end()
        painter = QPainter(self)
        painter.drawImage(0, 0, self.bkg_image)
        painter.end()

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        print(a0.localPos())
        for node in self.graph.nextNode():
            if abs(node.x() - a0.localPos().x()) < 20 and abs(node.y() - a0.localPos().y()) < 20:
                print(node)
                self.graph.highlightNodeSwitch(node)
        self.repaint()
        return super().mousePressEvent(a0)