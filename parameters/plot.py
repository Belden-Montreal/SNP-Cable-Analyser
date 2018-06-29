import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

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
        self._figure = plt.figure(figsize=(18.75,6.25), dpi=80) #might not work for all screen resolutions
        
        # define the different colors for this plot
        colors = iter(plt.cm.rainbow(np.linspace(0, 1, self._parameter.getNumPorts())))

        #get main and remote ports
        ends = dict()
        ends["main"] = ({port: (name, isRemote) for port,(name, isRemote) in self._parameter.getPorts().items() if isRemote is False})
        ends["remote"] = ({port: (name, isRemote) for port,(name, isRemote) in self._parameter.getPorts().items() if isRemote is True})

        for i, (isRemote, end) in enumerate(ends.items()):
            if len(end) > 0:
                ax = plt.subplot(1, len(ends), i+1)
                # set the labels
                plt.title(self._parameter.getName()+" : "+isRemote)
                plt.xlabel('Frequency (TODO)')
                plt.ylabel('dB')
                # draw each port's data
                for port, (name, isRemote) in end.items():
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
                        label=name, c=color
                    )

                ax.xaxis.set_major_formatter(ScalarFormatter())
                ax.grid(which="both")
                ax.legend(loc='upper left', ncol=1)
                if self._limit:
                    plt.semilogx(
                        *zip(*self._limit.evaluateArray({'f': self._parameter.getFrequencies()},
                                                        len(self._parameter.getFrequencies()), neg=True)),
                        c=color
                    )

    def setLimit(self, limit):
        self._limit = limit
        self._figure = None
        self.drawFigure()