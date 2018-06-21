import matplotlib.pyplot as plt

class ParameterPlot(object):
    def __init__(self, parameter, selection=[], limit=None):
        self._parameter = parameter
        self._figure = None
        self._selection = selection
        self._limit = limit

    def resetSelection(self):
        self._selection = []
        self.drawFigure()

    def addSelection(self, port):
        if port not in self._selection:
            self._selection.append(port)
        self.drawFigure()

    def removeSelection(self, port):
        if port in self._selection:
            self._selection.remove(port)
        self.drawFigure()

    def getSelection(self):
        return self._selection

    def getFigure(self):
        if self._figure is None:
            self.drawFigure()
        return self._figure

    def drawFigure(self):
        self._figure = plt.figure()
        
        # define the different colors for this plot
        colors = iter(plt.cm.rainbow(0, 1, self._parameter.getNumPorts()))

        # draw each port's data
        for port in self._parameter.getPorts():
            # get the next color
            if len(self._selection) != 0:
                if port not in self._selection:
                    color = 'grey'
                else:
                    color = next(colors)
            else:
                color = next(colors)

            # draw the data
            plt.semilogx(
                self._parameter.getFrequencies(),
                self._parameter.getParameter()[port],
                figure=self._figure, c=color
            )

        if self._limit:
            plt.semilogx(
                *zip(*self._limit.evaluateArray({'f': self._parameter.getFrequencies()},
                                                len(self._parameter.getFrequencies()), neg=True)),
                figure=self._figure, c=color
            )

        # set the labels
        plt.title(self._parameter.getName(), figure=self._figure)
        plt.xlabel('Frequency (TODO)', figure=self._figure)
        plt.ylabel('dB'              , figure=self._figure)

    def setLimit(self, limit):
        self._limit = limit
        self._figure = None
        self.drawFigure()