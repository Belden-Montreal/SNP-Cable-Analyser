from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 

class Canvas(FigureCanvas):
    def __init__(self, figure,  parent=None): 
        FigureCanvas.__init__(self, figure)
        self.setParent(parent)

    def changeFigure(self, figure):
        FigureCanvas.__init__(self, figure)

    
