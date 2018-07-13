from PyQt5 import QtWidgets
from widgets.tab_widget import TabWidget
from widgets import alien_widget_ui

class AlienWidget(TabWidget, alien_widget_ui.Ui_Form):
    def __init__(self):
        super(AlienWidget, self).__init__(self)
