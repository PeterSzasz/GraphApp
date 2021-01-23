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
        self.graphGen = GraphGenerator()
        self.renderer = GraphRender()
        self.setCentralWidget(self.renderer)
        self.numberOfNodes = 10
        self.numberOfRegionsX = 5
        self.numberOfRegionsY = 7
        self.connection_chance = 2
        self.randomStrategyList = ['Area Coordinates', 'Region Coordinates']
        self.randomClass1 = RandomCoords(self.numberOfNodes )
        self.randomClass2 = RandomRegionCoords(self.numberOfNodes,
                                                  self.numberOfRegionsX,
                                                  self.numberOfRegionsY)

        self.graphGen.setNodesStrategy(self.randomClass1)
        #self.graph = self.graphGen.genGraph(self.connection_chance,
        self.graph = self.graphGen.genGraph_Delaunay(self.renderer.area_w,
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
        nodeStratBox = QComboBox(toolBar)
        nodeStratBox.addItems(self.randomStrategyList)
        nodeStratBox.currentIndexChanged.connect(self.setNewNodeStrategy)
        toolBar.addWidget(nodeStratBox)
        edgeStratBox = QComboBox(toolBar)
        edgeStratBox.addItems(self.randomStrategyList)
        edgeStratBox.currentIndexChanged.connect(self.setNewEdgeStrategy)
        toolBar.addWidget(edgeStratBox)
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
        #self.graph = self.graphGen.genGraph(self.connection_chance,
        #                                    self.renderer.area_w,
        #                                    self.renderer.area_h)
        self.graph = self.graphGen.genGraph_Delaunay(self.renderer.area_w,
                                                     self.renderer.area_h)
        self.renderer.repaint()

    def setNewNodeStrategy(self, index: int):
        if index == 0:
            self.numberOfNodes = self.nodeNumber.value()
            self.randomClass1 = RandomCoords(self.numberOfNodes)
            self.graphGen.setNodesStrategy(self.randomClass1)
        elif index == 1:
            self.numberOfNodes = self.nodeNumber.value()
            self.numberOfRegionsX = self.regionNumberX.value()
            self.numberOfRegionsY = self.regionNumberY.value()
            self.randomClass2 = RandomRegionCoords(self.numberOfNodes,
                                                           self.numberOfRegionsX,
                                                           self.numberOfRegionsY)
            self.graphGen.setNodesStrategy(self.randomClass2)

    def setNewEdgeStrategy(self, index: int):
        if index == 0:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
    