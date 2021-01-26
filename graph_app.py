# PyQT5 app for graph visualization. Generating, searching, traversing, etc in one place.

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QGridLayout, QLabel, QMainWindow, QSpinBox, QStatusBar, QToolBar, QWidget
from PyQt5.QtWidgets import QApplication

from graph_render_widget import GraphRender
from graph_generator import GraphGenerator
from utilities.node_generator import RandomCoords, RandomRegionCoords

class MainWindow(QMainWindow):
    '''window for visualizing and controlling graphs'''

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Graph App")
        self.renderer = GraphRender()
        self.setCentralWidget(self.renderer)
        # set up graph generator and renderer
        self.graphGen = GraphGenerator()
        self.graphGen.area_h = self.renderer.area_h
        self.graphGen.area_w = self.renderer.area_w
        self.graph = self.graphGen.genGraph()
        self.renderer.setGraph(self.graph)
        # set up menus and bars
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
        toolBar.addWidget(QLabel("Node generator:"))
        nodeStratBox = QComboBox(toolBar)
        nodeStratBox.addItems(self.graphGen.nodeStrategyList)
        nodeStratBox.currentIndexChanged.connect(self.setNewNodeStrategy)
        toolBar.addWidget(nodeStratBox)
        toolBar.addWidget(QLabel("\nEdge generator:"))
        edgeStratBox = QComboBox(toolBar)
        edgeStratBox.addItems(self.graphGen.edgeStrategyList)
        edgeStratBox.currentIndexChanged.connect(self.setNewEdgeStrategy)
        toolBar.addWidget(edgeStratBox)
        toolBar.addSeparator()
        toolBar.addWidget(QLabel("Generator settings", toolBar))
        self.regionNumberX = QSpinBox()
        self.regionNumberX.setRange(1, 100)
        self.regionNumberX.setValue(self.graphGen.numberOfRegionsX)
        self.regionNumberX.valueChanged.connect(self.setNumberOfRegionsX)
        self.regionNumberY = QSpinBox()
        self.regionNumberY.setRange(1, 100)
        self.regionNumberY.setValue(self.graphGen.numberOfRegionsY)
        self.regionNumberY.valueChanged.connect(self.setNumberOfRegionsY)
        self.nodeNumber = QSpinBox()
        self.nodeNumber.setRange(1, 100)
        self.nodeNumber.setValue(self.graphGen.numberOfNodes)
        self.nodeNumber.valueChanged.connect(self.setNumberOfNodes)
        self.edgeChance = QSpinBox()
        self.edgeChance.setRange(0, 100)
        self.edgeChance.setValue(self.graphGen.connection_chance)
        self.edgeChance.valueChanged.connect(self.setConnectionChance)
        graphGrid = QGridLayout()
        graphGrid.setColumnMinimumWidth(0, 20)
        graphGrid.setColumnMinimumWidth(1, 30)
        graphGrid.addWidget(QLabel("Regions X:"))
        graphGrid.addWidget(self.regionNumberX)
        graphGrid.addWidget(QLabel("Regions Y:"))
        graphGrid.addWidget(self.regionNumberY)
        graphGrid.addWidget(QLabel("Node number:"))
        graphGrid.addWidget(self.nodeNumber)
        graphGrid.addWidget(QLabel("Edge forming\nchance:"))
        graphGrid.addWidget(self.edgeChance)
        graphGridHolder = QWidget()
        graphGridHolder.setLayout(graphGrid)
        toolBar.addWidget(graphGridHolder)
        toolBar.addSeparator()
        toolBar.addAction("Exit", self.close)
        return toolBar

    def newGraph(self):
        self.graph = self.graphGen.genGraph()
        self.renderer.repaint()

    def setNewNodeStrategy(self, index: int):
        self.graphGen.nodeStrategy = index

    def setNewEdgeStrategy(self, index: int):
        self.graphGen.edgeStrategy = index
    
    def setNumberOfNodes(self, value: int):
        self.graphGen.numberOfNodes = value

    def setConnectionChance(self, value: int):
        self.graphGen.connection_chance = value

    def setNumberOfRegionsX(self, value: int):
        self.graphGen.numberOfRegionsX = value

    def setNumberOfRegionsY(self, value: int):
        self.graphGen.numberOfRegionsY = value

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
    