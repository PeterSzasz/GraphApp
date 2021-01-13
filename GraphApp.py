# PyQT5 app for graph visualization. Generating, searching, traversing, etc in one place.

from GraphGenerator import GraphGenerator
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QPalette, QPen
from PyQt5.QtWidgets import QComboBox, QMainWindow, QPushButton, QStatusBar, QToolBar, QWidget
from PyQt5.QtWidgets import QApplication

from Core.graph import Edge, Graph, Node


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

    def paintEvent(self, a0: QPaintEvent) -> None:
        node_width = 8
        painter = QPainter(self)
        painter.setPen(QPen(Qt.darkGray, node_width//2))
        for edge in self.graph.nextEdge():
            painter.drawLine(edge.n1().x(), edge.n1().y(), edge.n2().x(), edge.n2().y())
        painter.setPen(QPen(Qt.black, node_width//2))
        for node in self.graph.nextNode():
            painter.drawEllipse(node.x() - node_width//2, node.y() - node_width//2, node_width, node_width)
        #return super().paintEvent(a0)


class MainWindow(QMainWindow):
    '''window for visualizing and controlling graphs'''

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Graph App")
        self.renderer = GraphRender()
        self.graphGen = GraphGenerator()
        self.graph = self.graphGen.genGraph(30,
                                            20,
                                            self.renderer.area_w,
                                            self.renderer.area_h)
        self.renderer.setGraph(self.graph)
        self.setCentralWidget(self.renderer)

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
        toolBar.addAction("Sorting")
        sortingBox = QComboBox(toolBar)
        sortingBox.addItems(['Quick', 'Merge', 'Bubble', 'Cocktail'])
        toolBar.addWidget(sortingBox)
        toolBar.addWidget(QPushButton("Sort", toolBar))
        toolBar.addSeparator()
        toolBar.addAction("Exit", self.close)
        return toolBar

    def newGraph(self):
        self.graph = self.graphGen.genGraph(30,
                                            20,
                                            self.renderer.area_w,
                                            self.renderer.area_h)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
    