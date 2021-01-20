# PyQT5 app for graph visualization. Generating, searching, traversing, etc in one place.

from GraphGenerator import GraphGenerator
import sys
import math
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPalette, QPen, QStaticText
from PyQt5.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSpinBox, QStatusBar, QToolBar, QWidget
from PyQt5.QtWidgets import QApplication

from Core.graph import Edge, Graph, Node
from Utilities import randoms

class GraphRender(QWidget):
    '''an area that can be used for drawing graphs, used within a Qt window/widget'''

    def __init__(self) -> None:
        super().__init__()
        self.area_w = 1024
        self.area_h = 768
        self.setMinimumSize(self.area_w, self.area_h)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

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

    def paintEvent(self, a0: QPaintEvent) -> None:
        node_width = 8
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # voronoi pixelate, kindof
        start_time = time.perf_counter()
        if self.graph.nodes:
            for x in range(0, self.area_w, 2):
                for y in range(0, self.area_h, 2):
                    dist = self.voronoiBackground(x, y)
                    dist = 255 - dist
                    if dist < 0: dist = 0
                    painter.setPen(QPen(QColor(dist, dist, dist, 255), 2))
                    painter.drawPoint(x, y)
        stop_time = time.perf_counter()
        print(stop_time - start_time)

        painter.setPen(QPen(Qt.white, node_width//2))
        painter.drawRect(0, 0, self.area_w, self.area_h)
        # draw the edges
        painter.setPen(QPen(Qt.darkGray, node_width//2))
        for edge in self.graph.nextEdge():
            painter.drawLine(edge.n1().x(),
                             edge.n1().y(),
                             edge.n2().x(),
                             edge.n2().y())
        # draw the nodes
        painter.setPen(QPen(Qt.black, node_width//2))
        for node in self.graph.nextNode():
            painter.drawEllipse(node.x() - node_width//2,
                                node.y() - node_width//2,
                                node_width,
                                node_width)
            painter.drawStaticText(node.x() - 30, node.y() + 5, QStaticText(str(node)))


class MainWindow(QMainWindow):
    '''window for visualizing and controlling graphs'''

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Graph App")
        self.graphGen = GraphGenerator()
        self.renderer = GraphRender()
        self.setCentralWidget(self.renderer)
        self.numberOfNodes = 10
        self.numberOfRegionsX = 5
        self.numberOfRegionsY = 7
        self.connection_chance = 2
        self.randomStrategyList = ['Area Coordinates', 'Region Coordinates']
        self.randomClass1 = randoms.RandomCoords(self.numberOfNodes )
        self.randomClass2 = randoms.RandomRegionCoords(self.numberOfNodes,
                                                  self.numberOfRegionsX,
                                                  self.numberOfRegionsY)

        self.graphGen.setRandomStrategy(self.randomClass1)
        self.graph = self.graphGen.genGraph(self.connection_chance,
                                            self.renderer.area_w,
                                            self.renderer.area_h)
        self.renderer.setGraph(self.graph)
        menu = self.menuBar().addMenu("&File")
        menu.addAction("&New")
        menu.addAction("&Save")
        menu.addAction("&Load")
        menu.addAction("E&xit", self.close)
        toolBar = self.createToolBar()
        toolBar.setOrientation(Qt.Vertical)
        self.addToolBar(Qt.RightToolBarArea, toolBar)
        statusBar = QStatusBar()
        statusBar.showMessage("Status Bar! More down to earth than Space Bar.")
        self.setStatusBar(statusBar)

    def createToolBar(self) -> QToolBar:
        toolBar = QToolBar(self)
        toolBar.addAction("New Graph", self.newGraph)
        toolBar.addSeparator()
        toolBar.addWidget(QLabel("Random strategy:"))
        randomStratBox = QComboBox(toolBar)
        randomStratBox.addItems(self.randomStrategyList)
        randomStratBox.currentIndexChanged.connect(self.setRandomStrategy)
        toolBar.addWidget(randomStratBox)
        toolBar.addSeparator()
        toolBar.addWidget(QLabel("Regions", toolBar))
        self.nodeNumber = QSpinBox()
        self.nodeNumber.setRange(1, 100)
        self.nodeNumber.setValue(self.numberOfNodes)
        self.regionNumberX = QSpinBox()
        self.regionNumberX.setRange(1, 100)
        self.regionNumberX.setValue(self.numberOfRegionsX)
        self.regionNumberY = QSpinBox()
        self.regionNumberY.setRange(1, 100)
        self.regionNumberY.setValue(self.numberOfRegionsY)
        self.edgeChance = QSpinBox()
        self.edgeChance.setRange(0, 100)
        self.edgeChance.setValue(self.connection_chance)
        graphGrid = QGridLayout()
        graphGrid.setColumnMinimumWidth(0, 25)
        graphGrid.setColumnMinimumWidth(1, 30)
        graphGrid.addWidget(QLabel("Node number:"))
        graphGrid.addWidget(self.nodeNumber)
        graphGrid.addWidget(QLabel("Regions X:"))
        graphGrid.addWidget(self.regionNumberX)
        graphGrid.addWidget(QLabel("Regions Y:"))
        graphGrid.addWidget(self.regionNumberY)
        graphGrid.addWidget(QLabel("Edge forming\nchance:"))
        graphGrid.addWidget(self.edgeChance)
        graphGridHolder = QWidget()
        graphGridHolder.setLayout(graphGrid)
        toolBar.addWidget(graphGridHolder)
        toolBar.addSeparator()
        toolBar.addAction("Exit", self.close)
        return toolBar

    def newGraph(self):
        self.connection_chance = self.edgeChance.value()
        self.graph = self.graphGen.genGraph(self.connection_chance,
                                            self.renderer.area_w,
                                            self.renderer.area_h)
        self.renderer.repaint()

    def setRandomStrategy(self, index: int):
        if index == 0:
            self.numberOfNodes = self.nodeNumber.value()
            self.randomClass1 = randoms.RandomCoords(self.numberOfNodes)
            self.graphGen.setRandomStrategy(self.randomClass1)
        elif index == 1:
            self.numberOfNodes = self.nodeNumber.value()
            self.numberOfRegionsX = self.regionNumberX.value()
            self.numberOfRegionsY = self.regionNumberY.value()
            self.randomClass2 = randoms.RandomRegionCoords(self.numberOfNodes,
                                                           self.numberOfRegionsX,
                                                           self.numberOfRegionsY)
            self.graphGen.setRandomStrategy(self.randomClass2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
    