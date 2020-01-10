from snpanalyzer.gui.ui.export.project import Ui_form

from PyQt5.QtCore import Qt, QVariant, QItemSelectionModel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ExportProjectWidget(QWidget):
    def __init__(self, parent=None):
        super(ExportProjectWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # setup config
        self.__config = None
        self.__model  = None
        self.__sample = None

    def __sampleStateChanged(self, item):
        # get the sample serie from the checked item
        sample = item.data()

        # add/remove the sample from the configuration
        if item.checkState() == Qt.Checked:
            self.__config.addSample(sample)
        else:
            self.__config.removeSample(sample)

        # disable the widget if we do not export this sample
        widgetConfig = self.__ui.sampleExportWidget.getConfiguration()
        if widgetConfig is not None:
            self.__ui.sampleExportWidget.setEnabled(widgetConfig.doExport())

    def __samplesSelectionChanged(self, current, previous):
        # make sure a model is setup
        if self.__model is None:
            return

        # get the sample
        sample = self.__model.itemFromIndex(current).data()
        if sample == self.__sample:
            return
        self.__sample = sample

        # get the configuration
        config = self.__config.getSamples()[sample]

        # change the configuration in the widget
        self.__ui.sampleExportWidget.setExportConfiguration(config)

        # disable the widget if we do not export this sample
        self.__ui.sampleExportWidget.setEnabled(config.doExport())

    def setExportConfiguration(self, config):
        # change configuration
        self.__config = config

        # remove selection signals
        if self.__ui.samplesListView.selectionModel() is not None:
            self.__ui.samplesListView.selectionModel().currentChanged.disconnect()

        # remove model signals
        if self.__ui.samplesListView.model() is not None:
            self.__ui.samplesListView.model().itemChanged.disconnect()

        # create the new model
        model = QStandardItemModel()
        for (sample, export) in config.getSamples().items():
            item = QStandardItem()
            item.setText(sample.getName())
            item.setCheckable(True)
            item.setCheckState(Qt.Checked if export.doExport() else Qt.Unchecked)
            item.setData(QVariant(sample))
            model.appendRow(item)
        model.itemChanged.connect(self.__sampleStateChanged)
        model.sort(0)
        
        # update the model of the list view
        self.__ui.samplesListView.setModel(model)
        self.__model = model

        # update selection signal
        self.__ui.samplesListView.selectionModel().currentChanged.connect(
            self.__samplesSelectionChanged
        )

        # select first sample by default
        self.__ui.samplesListView.setCurrentIndex(model.index(0, 0))

    def getConfiguration(self):
        return self.__config


        
