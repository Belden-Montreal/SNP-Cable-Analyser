from PyQt5 import QtWidgets
from widgets.tab_widget import TabWidget
from widgets import alien_widget_ui
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from canvas import Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class AlienWidget(TabWidget, alien_widget_ui.Ui_Form):
    def __init__(self, alien):
        super(AlienWidget, self).__init__(self)
        self._figure = Figure()
        self._alien = alien
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
        self.drawFigure("End 1", "PSANEXT")

    def updateWidget(self):
        test = self.testTypeGroup.checkedButton().text()
        end = self.endGroup.checkedButton().text()
        self.alienDisturbers.clear()
        for disturber in self._alien._disturbers[end][test]:
            item = QtWidgets.QListWidgetItem()
            item.setText(disturber.getName())
            self.alienDisturbers.addItem(item)
        self.drawFigure(end, test)

    def drawFigure(self, end, test):
        self._figure.clear()
        sample = self._alien._victims[end][test]
        if test == "PSANEXT":
            names = ["PSANEXT", "PSAACRN"]
        else:
            names = ["PSAFEXT", "PSAACRF"]
        if sample:
            params = [sample.getParameters()["PSAXEXT"], sample.getParameters()["PSAACRX"]]
            for i, param in enumerate(params):
                ax = self._figure.add_subplot(1,2,i+1)
                ax.set_title(end+" "+names[i])
                ax.set_xlabel("Frequency")
                ax.set_ylabel("dB")
                for port, (name, isRemote) in param.getPorts().items():
                    if not isRemote:
                        try:
                            data = list(map(lambda val: val[0], param.getParameter()[port]))
                        except:
                            data = param[port]
                        ax.semilogx(param.getFrequencies(),
                                    data,
                                    label=name)
                ax.xaxis.set_major_formatter(ScalarFormatter())
                ax.grid(which='both')
                ax.legend(loc='best')
        self.showTab()
    
    def showTab(self):
        self.graphicsView.draw()