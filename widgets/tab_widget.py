from PyQt5 import QtWidgets

class TabWidget(QtWidgets.QWidget):
    def __init__(self, ui):
        super(TabWidget, self).__init__()
        ui.setupUi(self)

    def getFigure(self):
        raise NotImplementedError