from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from snpanalyzer.gui.ui import dataFormatDialog
from PyQt5 import QtWidgets

class AlienNavigationToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, psaxextAnalysis, psaacrxAnalysis, parent=None):
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Parameter', 'Change alien parameter', 'subplots', 'change_parameter'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
        ) 
        super(AlienNavigationToolbar, self).__init__(canvas, parent)
        self._psaxextAnalysis = psaxextAnalysis
        self._psaacrxAnalysis = psaacrxAnalysis

    def change_parameter(self):
        if self._psaxextAnalysis and self._psaacrxAnalysis:
            dial = QtWidgets.QDialog(self)
            dial2 = dataFormatDialog.Ui_DataFormatDialog()
            dial2.setupUi(dial)
            dial.setWindowTitle("Change alien parameter")
            analyses = [self._psaxextAnalysis, self._psaacrxAnalysis]
            dial2.formatBox.addItems([f.getParameter().getName() for f in analyses])
            ok = dial.exec_()
            if ok:
                selectedFormat = dial2.formatBox.currentText()
                self.canvas.figure = (next(iter([f.getFigure() for f in analyses if f.getParameter().getName() == selectedFormat])))
                self.canvas.resize(*self.canvas.get_width_height())
                self.draw()