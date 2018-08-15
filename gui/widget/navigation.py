from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class NavigationToolbar(NavigationToolbar2QT):
    """
    This class is used for outputting navigation toolbar status to another label.
    """
    def __init__(self, canvas, parent, label, **kwargs):
        super(NavigationToolbar, self).__init__(canvas, parent, **kwargs)
        self.__label = label

    def set_message(self, s):
        self.__label.setText(s)

