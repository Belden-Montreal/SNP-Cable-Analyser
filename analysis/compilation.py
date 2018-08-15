from matplotlib import pyplot as plt
from analysis.format import DataFormat
from enum import Enum

def autoscale_y(axis, margin=0.1):
    """
    Taken from: https://stackoverflow.com/a/35094823
    """
    import numpy as np

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
        new_bot, new_top = get_bottom_top(line)
        if new_bot < bot: bot = new_bot
        if new_top > top: top = new_top

    axis.set_ylim(bot,top)

class PlotScale(Enum):
    LOGARITHMIC = 0
    LINEAR      = 1

class CompilationAnalysis(object):
    def __init__(self):
        self._format = None
        self._scale  = None

        self._samples = set()
        self._series = set()
        self._lines = dict()
        self._parameter = None

        self._figure = plt.figure()
        self._axis = self._figure.add_subplot(111)
        self._axis.set_xlabel("Frequency (Hz)")

        plt.tight_layout()

        self.setScale(PlotScale.LOGARITHMIC)
        self.setFormat(DataFormat.MAGNITUDE)

    def __getData(self, parameter, serie):
        # get the frequencies
        frequencies = parameter.getFrequencies()

        # format the data
        data = list()
        if self._format == DataFormat.MAGNITUDE:
            data = [mag for (mag,_) in parameter.getParameter()[serie]]
        elif self._format == DataFormat.PHASE:
            data = [phase for (_,phase) in parameter.getParameter()[serie]]
        elif self._format == DataFormat.REAL:
            data = [value.real for value in parameter.getComplexParameter()[serie]]
        elif self._format == DataFormat.IMAGINARY:
            data = [value.imag for value in parameter.getComplexParameter()[serie]]

        return (frequencies, data)

    def __addLine(self, sample, serie):
        # make sure a parameter is specified
        if self._parameter is None:
            return

        # create the list of lines for this sample if necessary
        if sample not in self._lines:
            self._lines[sample] = dict()

        # get the parameter from the sample
        parameter = sample.getParameter(self._parameter)

        # get the data from the sample
        (frequencies, data) = self.__getData(parameter, serie)

        # plot the line
        label="{} / {}".format(sample.getName(), serie.getName())
        self._lines[sample][serie] = self._axis.plot(
            frequencies, data,
            label=label,
            linewidth=0.8
        )

        # scale y axis to fit data
        autoscale_y(self._axis)

    def __removeLine(self, sample, serie, keepsample=False):
        # make sure the sample have series
        if sample not in self._lines:
            return
        # add the serie into the set of series
        self._series.add(serie)
        # make sure the sample have this serie
        if serie not in self._lines[sample]:
            return

        # remove the line from this serie
        lines = self._lines[sample].pop(serie)
        for line in lines:
            line.remove()

        # remove the sample from the lines if it is empty
        if not keepsample:
            if len(self._lines[sample]) == 0:
                self._lines.pop(sample)

    def addSample(self, sample):
        # don't add the sample if it is already there
        if sample in self._samples:
            return

        # add the sample into the set of samples
        self._samples.add(sample)

        # add all the series for this sample
        for serie in self._series:
            self.__addLine(sample, serie)

    def removeSample(self, sample):
        # make sure the sample is in the compilation
        if sample not in self._samples:
            return

        # remove all series for this sample
        for serie in self._series:
            self.__removeLine(sample, serie)

        # remove the sample from the compilation
        self._samples.discard(sample)

    def addSerie(self, serie):
        # don't add the serie if it is already in the compilation
        if serie in self._series:
            return

        # add the serie into the set of series
        self._series.add(serie)

        # add the serie for all samples
        for sample in self._samples:
            self.__addLine(sample, serie)

    def removeSerie(self, serie):
        # make sure the serie is in the compilation
        if serie not in self._series:
            return

        # remove this serie from all samples
        for sample in self._samples:
            self.__removeLine(sample, serie)

        # remove the serie from the compilation
        self._series.discard(serie)

    def setTitle(self, title):
        self._axis.set_title(title)

    def setParameter(self, parameter):
        # make sure the parameter is different
        if parameter == self._parameter:
            return

        # update the parameter
        self._parameter = parameter

        # remove all lines in the graph
        for sample in self._samples:
            for serie in self._series:
                self.__removeLine(sample, serie, keepsample=True)
        self._series = set()

    def getParameter(self, parameter):
        return self._parameter

    def setFormat(self, pformat):
        # make sure the format changed
        if self._format == pformat:
            return

        # update the format
        self._format = pformat

        # replace all lines in the graph
        for sample in self._samples:
            for serie in self._series:
                self.__removeLine(sample, serie)
                self.__addLine(sample, serie)

        # set y axis label
        if self._format == DataFormat.MAGNITUDE:
            self._axis.set_ylabel("Magnitude (dB)")
        elif self._format == DataFormat.PHASE:
            self._axis.set_ylabel("Phase")
        elif self._format == DataFormat.REAL:
            self._axis.set_ylabel("Real")
        elif self._format == DataFormat.IMAGINARY:
            self._axis.set_ylabel("Imaginary")

    def getFormat(self):
        return self._format

    def setScale(self, scale):
        # make sure the scale changed
        if self._scale == scale:
            return

        # update the scale
        self._scale = scale

        # change the plot scale
        if self._scale == PlotScale.LOGARITHMIC:
            self._axis.set_xscale("log")
        else:
            self._axis.set_xscale("linear")

    def getScale(self):
        return self._scale

    def getFigure(self):
        return self._figure
