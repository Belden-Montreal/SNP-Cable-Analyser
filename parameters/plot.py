import matplotlib.pyplot as plt
# plt.rcParams.update({'figure.max_open_warning': 0})
from matplotlib.figure import Figure
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

        #get main and remote ports
        ends = dict()
        ends["main"] = ({serie for serie in self._parameter.getDataSeries() if serie.isRemote() is False})
        ends["remote"] = ({serie for serie in self._parameter.getDataSeries() if serie.isRemote() is True})

        for i, (isRemote, end) in enumerate(ends.items()):
            if len(end) > 0:
                # define the different colors for this plot
                colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(end)+1)))
                ax = self._figure.add_subplot(1, len(ends), i+1)
                # set the labels
                ax.set_title(self._parameter.getName()+" : "+isRemote)
                ax.set_xlabel('Frequency (TODO)')
                ax.set_ylabel('dB')
                # draw each port's data
                for serie in end:
                    # get the next color
                    if len(self._selection) != 0:
                        if serie.getPort() not in self._selection:
                            color = 'grey'
                        else:
                            color = next(colors)
                    else:
                        color = next(colors)

                    try:
                        data = list(map(lambda val: val[0], self._parameter.getParameter()[serie]))
                    except:
                        data = self._parameter.getParameter()[serie]
                    # draw the data
                    ax.semilogx(
                        self._parameter.getFrequencies(),
                        data,
                        label=serie.getName(), c=color
                    )

                ax.xaxis.set_major_formatter(ScalarFormatter())
                ax.grid(which="both")
                if self._limit:
                    try:
                        ax.semilogx(
                            *zip(*self._limit.evaluateArray({'f': self._parameter.getFrequencies()},
                                                            len(self._parameter.getFrequencies()), neg=True)),
                            label="limit", c=next(colors), linestyle="--"
                        )
                    except:
                        print(len(self._limit.functions))                       
                ax.legend(loc='best')

    def setLimit(self, limit):
        self._limit = limit
        self._figure = None
        self.drawFigure()
