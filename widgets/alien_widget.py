from PyQt5 import QtWidgets, QtCore
from widgets.tab_widget import TabWidget
from widgets import alien_widget_ui
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import numpy as np
from canvas import Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class AlienWidget(TabWidget, alien_widget_ui.Ui_Form):
    def __init__(self, alienNode):
        super(AlienWidget, self).__init__(self)
        self._figure = Figure()
        self._alien = alienNode.getObject()
        self._node = alienNode
        self.graphicsView = Canvas(self._figure)
        self.verticalLayout.insertWidget(0, self.graphicsView)
        self.navBar = NavigationToolbar(self.graphicsView, self)
        self.verticalLayout.insertWidget(1, self.navBar)
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
        self._hiddenPorts = list()
        self.alien12.toggled.connect(lambda: self.portsChanged())
        self.alien36.toggled.connect(lambda: self.portsChanged())
        self.alien45.toggled.connect(lambda: self.portsChanged())
        self.alien78.toggled.connect(lambda: self.portsChanged())
        self.alienLimitCheck.toggled.connect(lambda: self.showLimit())
        self.alienAvgLimitCheck.toggled.connect(lambda: self.showLimit(True))
        self.alienAvg.toggled.connect(lambda: self.showAverage())
        self._showLimit = True
        self._showAvgLimit = True
        self._showAvg = True
        self.portsChanged()
        
    def updateWidget(self):
        end, test = self.getCheckButtons()
        self.alienDisturbers.clear()
        for disturber in self._alien.disturbers()[test][end]:
            item = QtWidgets.QListWidgetItem()
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            item.setText(disturber.getName())
            self.alienDisturbers.addItem(item)
        self.drawFigure(end, test)

    def drawFigure(self, end, test):
        self._figure.clear()
        sample = self._alien.victims()[test][end]
        if test == "PSANEXT":
            names = ["PSANEXT", "PSAACRN"]
        else:
            names = ["PSAFEXT", "PSAACRF"]
        if sample:
            params = [sample.getParameters()[names[0]], sample.getParameters()[names[1]]]
            for i, param in enumerate(params):
                colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(param.getPorts())+3)))

                ax = self._figure.add_subplot(1,2,i+1)
                ax.set_title(end+" "+names[i])
                ax.set_xlabel("Frequency")
                ax.set_ylabel("dB")
                avg = np.array(list())
                for port, (name, isRemote) in param.getPorts().items():
                    color = next(colors)
                    if not isRemote:
                        try:
                            data = list(map(lambda val: val[0], param.getParameter()[port]))
                        except:
                            data = param[port]
                        if len(avg) == 0:
                            avg = np.array(data)
                        else:
                            avg = np.add(avg, data)
                        if name not in self._hiddenPorts:
                            ax.semilogx(param.getFrequencies(),
                                        data,
                                        label=name, c=color)

                limit = param.getLimit()
                avg = avg/(len(param.getPorts()))
                if self._showAvg:
                    color = next(colors)
                    ax.semilogx(
                        param.getFrequencies(),
                        avg,
                        label="average", c=color,)
                if self._showLimit and limit:
                    color = next(colors)
                    ax.semilogx(
                        *zip(*limit.evaluateArray({'f': param.getFrequencies()}, len(param.getFrequencies()), neg=True)),
                        label="limit", c=color,
                        linestyle="--")
                if self._showAvgLimit and sample.getStandard():
                    if "AVG"+names[i] in sample.getStandard().limits:
                        limit = sample.getStandard().limits["AVG"+names[i]]
                        if limit:
                            color = next(colors)
                            ax.semilogx(
                                *zip(*limit.evaluateArray({'f': param.getFrequencies()}, len(param.getFrequencies()), neg=True)),
                                label="average limit", c=color,
                                linestyle="--")
                ax.xaxis.set_major_formatter(ScalarFormatter())
                ax.grid(which='both')
                ax.legend(loc='best')
        self.showTab()

    def importVictim(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select victim", "", "sNp Files (*.s*p)")
        end, test = self.getCheckButtons()
        sample = self._alien.importSamples([fileName], end, test, disturber=False)
        self._node.addChildren([sample], end, test)
        self.updateWidget()

    def importDisturbers(self):
        files,_ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select disturbers", "", "sNp Files (*.s*p)")
        end, test = self.getCheckButtons()
        samples = self._alien.importSamples(files, end, test, disturber=True)
        self._node.addChildren(samples, end, test)
        self.updateWidget()

    def disturbersChanged(self):
        disturbers = list()
        for i in range(self.alienDisturbers.count()):
            item = self.alienDisturbers.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                disturbers.append(item.text())
        end, test = self.getCheckButtons()
        self._alien.updateDisturbers(disturbers, end, test)
        self.drawFigure(end, test)

    def portsChanged(self):
        end, test = self.getCheckButtons()
        self._hiddenPorts = list()
        if not self.alien12.isChecked():
            self._hiddenPorts.append(self.alien12.text())
        if not self.alien45.isChecked():
            self._hiddenPorts.append(self.alien45.text())
        if not self.alien36.isChecked():
            self._hiddenPorts.append(self.alien36.text())
        if not self.alien78.isChecked():
            self._hiddenPorts.append(self.alien78.text())
        self.drawFigure(end, test)

    def showLimit(self, average=False):
        if average:
            self._showAvgLimit = not self._showAvgLimit
        else:
            self._showLimit = not self._showLimit
        end, test = self.getCheckButtons()
        self.drawFigure(end, test)
    
    def showAverage(self):
        self._showAvg = not self._showAvg
        end, test = self.getCheckButtons()
        self.drawFigure(end, test)

    def getCheckButtons(self):
        test = self.testTypeGroup.checkedButton().text()
        end = self.endGroup.checkedButton().text()
        return end, test