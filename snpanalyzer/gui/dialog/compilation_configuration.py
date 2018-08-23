from snpanalyzer.gui.ui.compilation_configuration import Ui_dialog
from snpanalyzer.gui.widget.navigation import NavigationToolbar
from snpanalyzer.analysis.compilation import CompilationAnalysis
from snpanalyzer.analysis.scale import PlotScale
from snpanalyzer.analysis.format import DataFormat

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QSizePolicy
from PyQt5.QtWidgets import QDialogButtonBox, QHBoxLayout, QSpacerItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class CompilationConfigurationDialog(QDialog):
    def __init__(self, samples, compilation=None):
        super(CompilationConfigurationDialog, self).__init__()
        self.__samples = samples
        self.__ui = Ui_dialog()
        self.__ui.setupUi(self)

        # create the compilation if needed
        if compilation is None:
            self._compilation = CompilationAnalysis()
        else:
            self._compilation = compilation

        # use compilation's figure
        self.__setFigure(self._compilation.getFigure())

        # setup different sections of the dialog
        self.__setupTitleLineEdit()
        self.__setupParameters()
        self.__setupSamples()
        self.__setupFormats()
        self.__setupScale()
        self.__setupButtons()

        # set default selection
        self.__ui.parameterComboBox.setCurrentIndex(1)

    def __setFigure(self, figure):
        # remove current widgets in layouts
        for i in reversed(range(self.__ui.graphicVerticalLayout.count())):
            widget = self.__ui.graphicVerticalLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # transparent background
        figure.patch.set_facecolor("None")

        # create the canvas
        self.__canvas = FigureCanvasQTAgg(figure)
        self.__canvas.setStyleSheet("background-color:transparent;")

        # add the canvas to the layout
        self.__ui.graphicVerticalLayout.addWidget(self.__canvas)

        # add the navigation toolbar
        navig = NavigationToolbar(self.__canvas, None, self.__ui.graphicTextLabel)
        layout = QHBoxLayout()
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(navig)
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.__ui.graphicVerticalLayout.addLayout(layout)

    def __setupTitleLineEdit(self):
        self.__ui.titleLineEdit.textEdited.connect(self.__setTitle)
        self.__ui.titleLineEdit.textChanged.connect(self.__setTitle)

    def __setupParameters(self):
        # find all parameters in all samples
        parameters = dict()
        for sample in self.__samples:
            for (ptype, parameter) in sample.getParameters().items():
                name = parameter.getName()
                formats = parameter.getAvailableFormats()
                parameters[ptype] = (name, formats)

        # clear the combo box
        self.__ui.parameterComboBox.clear()

        # setup the combo box
        for ptype in parameters:
            (pname, formats) = parameters[ptype]
            self.__ui.parameterComboBox.addItem(pname, userData = ptype)
        self.__ui.parameterComboBox.model().sort(0)

        # connect the index changed signal
        self.__ui.parameterComboBox.currentIndexChanged.connect(
            lambda index: self.__setParameter(index, parameters)
        )

    def __setupSamples(self):
        # create the model for the list box
        model = QStandardItemModel()
        for sample in self.__samples:
            item = QStandardItem()
            item.setText(sample.getName())
            item.setCheckable(True)
            item.setData(QVariant(sample))
            model.appendRow(item)
        model.itemChanged.connect(self.__sampleStateChanged)
        model.sort(0)
        self.__ui.samplesListView.setModel(model)

    def __setupFormats(self):
        self.__ui.formatSelection.changed.connect(self.__setFormat)

    def __setupScale(self):
        self.__ui.scaleSelection.changed.connect(self.__setScale)
        self.__ui.scaleSelection.setScale(self._compilation.getScale())

    def __setupButtons(self):
        # setup the ok and cancel buttons
        self.__ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.__ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

    def __setParameter(self, index, data):
        # get the selected parameter
        self.__parameter = self.__ui.parameterComboBox.itemData(index)
        (names, formats) = data[self.__parameter]

        # change available formats
        self.__ui.formatSelection.setAvailableFormats(formats)

        # update the title
        self.__ui.titleLineEdit.setText(names)

        # get all the data series
        series = set()
        for sample in self.__samples:
            series.update(sample.getParameter(self.__parameter).getDataSeries())

        # create the model for the list box
        model = QStandardItemModel()
        for serie in series:
            item = QStandardItem()
            item.setText(serie.getName())
            item.setCheckable(True)
            item.setData(QVariant(serie))
            model.appendRow(item)
        model.itemChanged.connect(self.__serieStateChanged)
        model.sort(0)
        self.__ui.dataseriesListView.setModel(model)

        # change the parameter in the compilation
        self._compilation.setParameter(self.__parameter)

        # update the graph
        self.__canvas.draw()

    def __serieStateChanged(self, item):
        # get the serie from the checked item
        serie = item.data()

        # add/remove corresponding serie
        if item.checkState() == Qt.Checked:
            self._compilation.addSerie(serie)
        else:
            self._compilation.removeSerie(serie)

        # update the graph
        self.__canvas.draw()

    def __sampleStateChanged(self, item):
        # get the sample from the checked item
        sample = item.data()

        # add/remove corresponding sample
        if item.checkState() == Qt.Checked:
            self._compilation.addSample(sample)
        else:
            self._compilation.removeSample(sample)

        # update the graph
        self.__canvas.draw()

    def __setTitle(self, title):
        # set the title
        self._compilation.setTitle(str(title))

        # update the graph
        self.__canvas.draw()

    def __setFormat(self, pformat):
        # change the format
        self._compilation.setFormat(pformat)

        # update the graph
        self.__canvas.draw()

    def __setScale(self, scale):
        # change the scale
        self._compilation.setScale(scale)

        # update the graph
        self.__canvas.draw()
