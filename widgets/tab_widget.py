from PyQt5 import QtWidgets
from matplotlib.figure import Figure

class TabWidget(QtWidgets.QWidget):
    def __init__(self, ui):
        super(TabWidget, self).__init__()
        ui.setupUi(self)

    def __initWidgetOnly__(self, parent):
        super(TabWidget, self).__init__()
        