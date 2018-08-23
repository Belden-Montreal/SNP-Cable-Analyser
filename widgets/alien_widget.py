from PyQt5 import QtWidgets, QtCore
from widgets.tab_widget import TabWidget
from widgets import alien_widget_ui
from parameters.type import ParameterType
import numpy as np
from canvas import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class AlienWidget(TabWidget, alien_widget_ui.Ui_Form):
    def __init__(self, alienNode, vnaManager):
        super(AlienWidget, self).__init__(self)
        self._alien = alienNode.getObject()
        self._node = alienNode
        self.testTypeGroup = QtWidgets.QButtonGroup(self)
        self.testTypeGroup.addButton(self.alienPSANEXT)
        self.testTypeGroup.addButton(self.alienPSAACRF)
        self.testTypeGroup.buttonClicked.connect(lambda: self.updateWidget())
        self.endGroup = QtWidgets.QButtonGroup(self)
        self.endGroup.addButton(self.alienEnd1)
        self.endGroup.addButton(self.alienEnd2)
        self.endGroup.buttonClicked.connect(lambda: self.updateWidget())
        self.alienVictimButton.clicked.connect(lambda: self.importVictim())
        self.alienImportSNP.clicked.connect(lambda: self.importDisturbers())
        self.alienDisturbers.itemChanged.connect(lambda: self.disturbersChanged())
        self.alien12.toggled.connect(lambda: self.updateStateDraw())
        self.alien36.toggled.connect(lambda: self.updateStateDraw())
        self.alien45.toggled.connect(lambda: self.updateStateDraw())
        self.alien78.toggled.connect(lambda: self.updateStateDraw())
        self.alienLimitCheck.toggled.connect(lambda: self.updateStateDraw())
        self.alienAvgLimitCheck.toggled.connect(lambda: self.updateStateDraw())
        self.alienAvg.toggled.connect(lambda: self.updateStateDraw())
        self._vna = vnaManager
        self._vna.connection.connect(lambda: self.connect())
        self.alienRun.clicked.connect(lambda: self.acquireDisturbers())
        self.victimRun.clicked.connect(lambda: self.acquireVictim())
        self._analysis, self._analysis2 = None, None
        self.graphicsView = Canvas(Figure())
        self.verticalLayout.insertWidget(0, self.graphicsView)
        self.navBar = NavigationToolbar(self.graphicsView, self)
        self.verticalLayout.insertWidget(1, self.navBar)
        end, test = self.getCheckButtons()
        self.changeFigure(end, test)
        self.connect()

    def connect(self):
        self.alienRun.setEnabled(self._vna.connected())
        self.victimRun.setEnabled(self._vna.connected())
        
    def updateWidget(self):
        end, test = self.getCheckButtons()
        self._alien.resetDisturbers(end, test)
        self.alienDisturbers.clear()
        for disturber in self._alien.disturbers()[test][end]:
            item = QtWidgets.QListWidgetItem()
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            item.setText(disturber.getName())
            self.alienDisturbers.addItem(item)
        if self._alien.victims()[test][end]:
            self.victimLabel.setText(self._alien.victims()[test][end].getName())
        else:
            self.victimLabel.setText("\"\"")
        self.changeFigure(end, test)
        self.updateState()

    def changeFigure(self, end, test):
        #Remove figure and navbar
        for i in reversed(range(2)):
            widget = self.verticalLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        #Re-add the figure
        self._analysis, self._analysis2 = self._alien.getCurrentAnalyses(test, end)
        if self._analysis:
            figure = self._analysis.getFigure()
        else:
            figure = Figure()
        self.graphicsView = Canvas(figure)
        self.verticalLayout.insertWidget(0, self.graphicsView)
        self.navBar = NavigationToolbar(self.graphicsView, self)
        self.verticalLayout.insertWidget(1, self.navBar)
        self.graphicsView.draw()

    def importVictim(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select victim", "", "sNp Files (*.s*p)")
        if fileName:
            end, test = self.getCheckButtons()
            self._alien.importSamples([fileName], end, test, disturber=False)
            self._node.updateChildren()
            self.victimLabel.setText(self._alien.victims()[test][end].getName())
            self.changeFigure(end, test)

    def acquireVictim(self):
        fileName = self._vna.acquire()
        if fileName:
            end, test = self.getCheckButtons()
            self._alien.importSamples([fileName], end, test, disturber=False)
            self._node.updateChildren()
            self.victimLabel.setText(self._alien.victims()[test][end].getName())
            self.changeFigure(end, test)

    def importDisturbers(self):
        files,_ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select disturbers", "", "sNp Files (*.s*p)")
        if files:
            end, test = self.getCheckButtons()
            self._alien.importSamples(files, end, test, disturber=True)
            self._node.updateChildren()
            self.updateWidget()

    def acquireDisturbers(self):
        n, ok = QtWidgets.QInputDialog.getInt(self, "Number of disturbers", "Please enter the number of disturbers to acquire", 1, 1, 32)
        files = list()
        if ok:
            for _ in range(n):
                fileName = self._vna.acquire()
                if fileName:
                    files.append(fileName)
            end, test = self.getCheckButtons()
            self._alien.importSamples(files, end, test, disturber=True)
            self._node.updateChildren()
            self.updateWidget()

    def disturbersChanged(self):
        disturbers = list()
        for i in range(self.alienDisturbers.count()):
            item = self.alienDisturbers.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                disturbers.append(item.text())
        end, test = self.getCheckButtons()
        self._alien.updateDisturbers(disturbers, end, test)
        self.changeFigure(end, test)

    def updateState(self):
        self.setPorts()
        self.setLimit()
        self.setAverage()

    def updateStateDraw(self):
        self.updateState()
        self.graphicsView.draw()

    def setPorts(self):
        hiddenPorts = list()
        if not self.alien12.isChecked():
            hiddenPorts.append(self.alien12.text())
        if not self.alien45.isChecked():
            hiddenPorts.append(self.alien45.text())
        if not self.alien36.isChecked():
            hiddenPorts.append(self.alien36.text())
        if not self.alien78.isChecked():
            hiddenPorts.append(self.alien78.text())
        if self._analysis:
            for serie in self._analysis.getParameter().getDataSeries():
                if serie.getName() in hiddenPorts:
                    self._analysis.removeSerie(serie)
                else:
                    self._analysis.addSerie(serie)
    
    def setLimit(self):
        showAvgLimit = self.alienAvgLimitCheck.isChecked()
        showLimit = self.alienLimitCheck.isChecked()
        if self._analysis:
            if showLimit:
                self._analysis.addLimit()
            else:
                self._analysis.removeLimit()
            if showAvgLimit:
                self._analysis.addAverageLimit()
            else:
                self._analysis.removeAverageLimit()

    def setAverage(self):
        showAvg = self.alienAvg.isChecked()
        if showAvg:
            self._analysis.addAverage()
        else:
            self._analysis.removeAverage()

    def getCheckButtons(self):
        test = self.testTypeGroup.checkedButton().text()
        end = self.endGroup.checkedButton().text()
        return end, test