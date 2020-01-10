import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
from matplotlib.ticker import ScalarFormatter
from snpanalyzer.parameters.plot import ParameterPlot
import numpy as np

class CasePlot(ParameterPlot):
    def __init__(self, parameter, selection=[], limit=None):
        super(CasePlot, self).__init__(parameter, selection, limit)

    def drawFigure(self):
        self._figure = plt.figure(figsize=(18.75,6.25), dpi=100) #might not work for all screen resolutions
        print("DRAWING FIGURE")
        for i, (port, (name,_)) in enumerate(self._parameter.getPorts().items()):

            portData = self._parameter.getParameter()[port]
            # define the different colors for this plot
            colors = iter(plt.cm.rainbow(np.linspace(0, 1, len(portData)+1)))
            ax = plt.subplot(2, len(self._parameter.getPorts())//2, i+1)
            # set the labels
            plt.title(name)
            plt.xlabel('Frequency (TODO)')
            plt.ylabel('dB')
            # draw each port's data
            for n, data in portData.items():
                # get the next color
                if len(self._selection) != 0:
                    # if port not in self._selection:
                    #     color = 'grey'
                    # else:
                    color = next(colors)
                else:
                    color = next(colors)

                plotData = list(map(lambda val: val[0], data))

                # draw the data
                plt.semilogx(
                    self._parameter.getFrequencies(),
                    plotData,
                    label="Case "+str(n), c=color
                )

            ax.xaxis.set_major_formatter(ScalarFormatter())
            ax.grid(which="both")
            if self._limit:
                plt.semilogx(
                    *zip(*self._limit.evaluateArray({'f': self._parameter.getFrequencies()},
                                                    len(self._parameter.getFrequencies()), neg=True)),
                    label="limit", c=next(colors), linestyle="--"
                )
            ax.legend(loc='best')
