from PyQt5 import QtWidgets
from widgets import alien_widget_ui

class AlienWidget(QtWidgets.QWidget, alien_widget_ui.Ui_Form):
    def __init__(self):
        super(AlienWidget, self).__init__()
        self.setupUi(self)
