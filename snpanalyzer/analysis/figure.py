from snpanalyzer.analysis.analysis import Analysis
from snpanalyzer.analysis.scale import PlotScale

import matplotlib.pyplot as plt
import numpy as np

def autoscaleY(axis, margin=0.1):
    """
    Taken from: https://stackoverflow.com/a/35094823
    """

    def get_bottom_top(line):
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo,hi = axis.get_xlim()
        y_displayed = yd[((xd>lo) & (xd<hi))]
        h = np.max(y_displayed) - np.min(y_displayed)
        bot = np.min(y_displayed)-margin*h
        top = np.max(y_displayed)+margin*h
        return bot,top

    lines = axis.get_lines()
    bot,top = np.inf, -np.inf

    for line in lines:
        try:
            new_bot, new_top = get_bottom_top(line)
        except ValueError as error:
            print(error)
            return
        if new_bot < bot: bot = new_bot
        if new_top > top: top = new_top
    limits = np.array([bot, top], dtype=np.float64)
    axis.set_ylim(limits)

class FigureAnalysis(Analysis):
    def __init__(self, figure=None, axis=None, **kwargs):
        super(FigureAnalysis, self).__init__(**kwargs)

        self._format = None
        self._scale  = None
        self._lines  = dict()
        self._colors = dict()
        self._colormap = iter(plt.cm.rainbow(
            np.linspace(0, 1, self.getMaximumNumberOfLines()+1)
        ))
        
        # create the figure if needed
        if figure is None and axis is None:
            (self._figure, self._axis) = plt.subplots()
        else:
            self._figure = figure
            self._axis = axis
        self._legend = None

        # default scale and format
        self.setTitle(self.getDefaultTitle())
        self.setScale(self.getDefaultScale())
        self.setFormat(self.getDefaultFormat())

        # default labels
        self._setXLabel()
        self._setYLabel()

    def _setXLabel(self):
        self._axis.set_xlabel("Frequency (MHz)")

    def _setYLabel(self):
        self._axis.set_ylabel(self._format.getTitle())

    def _updateLegend(self):
        if self._legend is not None:
            self._legend.remove()
        self._legend = self._axis.legend(loc='best', ncol=3)

    def _addLine(self, identifier):
        # make sure the identifier isn't already in the lines
        if identifier in self._lines:
            return

        # get the color of the line
        color = None
        if identifier in self._colors:
            color = self._colors[identifier]
        else:
            color = next(self._colormap)
            self._colors[identifier] = color

        # get the data
        x = self._getXData(identifier)
        y = self._getYData(identifier)
        label = self._getLabel(identifier)

        # add the line
        self._lines[identifier] = self._axis.plot(
            x, y,
            label=label,
            linewidth=0.6,
            c=color,
            linestyle=self._getLineStyle(identifier)
        )
        
        # scale Y axis to fit data
        autoscaleY(self._axis)

        # update the legend
        self._updateLegend()

    def _removeLine(self, identifier):
        # make sure the serie in preset
        if identifier not in self._lines:
            return

        # remove the line
        {line.remove() for line in self._lines.pop(identifier)}

        # update the legend
        self._updateLegend()

    def _getXData(self, identifier):
        raise NotImplementedError

    def _getYData(self, identifier):
        raise NotImplementedError

    def _getLabel(self, identifier):
        raise NotImplementedError

    def _getLineStyle(self, identifier):
        raise NotImplementedError

    def getDefaultTitle(self):
        raise NotImplementedError

    def getDefaultScale(self):
        raise NotImplementedError

    def getDefaultFormat(self):
        raise NotImplementedError

    def getMaximumNumberOfLines(self):
        raise NotImplementedError

    def getAvailableFormats(self):
        raise NotImplementedError

    def setScale(self, scale):
        # make sure scale changed
        if self._scale == scale:
            return

        # update the scale
        self._scale = scale

        # change the plot scale
        if self._scale == PlotScale.LOGARITHMIC:
            self._axis.set_xscale("log")
        else:
            self._axis.set_xscale("linear")

    def setFormat(self, pformat):
        # make sure the format changed
        if self._format == pformat:
            return

        # make sure the format is supported
        if pformat not in self.getAvailableFormats():
            return

        # update the format
        self._format = pformat

        # replace all lines in the figure
        for identifier in self._lines:
            self._removeLine(identifier)
            self._addLine(identifier)

        # set Y axis label
        self._setYLabel()

    def setTitle(self, title):
        self._axis.set_title(title)

    def getFormat(self):
        return self._format

    def getFigure(self):
        return self._figure
