from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from widgets import dataFormatDialog
from PyQt5 import QtWidgets

class NavigationToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, analysis, parent=None):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Format', 'Change data format', 'subplots', 'change_format'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
        ) 
        super(NavigationToolbar, self).__init__(canvas, parent)
        self._analysis = analysis

    def change_format(self):
        if self._analysis:
            dial = QtWidgets.QDialog(self)
            dial2 = dataFormatDialog.Ui_DataFormatDialog()
            dial2.setupUi(dial)
            formats = self._analysis.getAvailableFormats()
            dial2.formatBox.addItems([f.getName() for f in formats])
            ok = dial.exec_()
            if ok:
                selectedFormat = dial2.formatBox.currentText()
                self._analysis.setFormat(next(iter([f for f in formats if f.getName() == selectedFormat]), self._analysis.getDefaultFormat()))
                self.draw()