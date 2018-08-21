from gui.ui.export.parameter import Ui_form

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ExportParameterWidget(QWidget):
    def __init__(self, parent=None):
        super(ExportParameterWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # setup signals
        self.__config = None
        self.__ui.scaleSelection.changed.connect(self.__setScale)
        self.__ui.formatSelection.changed.connect(self.__setFormat)

    def __serieStateChanged(self, item):
        # get the data serie from the checked item
        serie = item.data()

        # add/remove the data serie from the configuration
        if item.checkState() == Qt.Checked:
            self.__config.addDataSerie(serie)
        else:
            self.__config.removeDataSerie(serie)

    def __setScale(self, scale):
        if self.__config is not None:
            self.__config.setScale(scale)

    def __setFormat(self, pformat):
        if self.__config is not None:
            self.__config.setFormat(pformat)

    def setExportConfiguration(self, config):
        # change configuration
        self.__config = config

        # create the new model
        model = QStandardItemModel()
        for (serie, state) in config.getDataSeries().items():
            item = QStandardItem()
            item.setText(serie.getName())
            item.setCheckable(True)
            item.setCheckState(Qt.Checked if state else Qt.Unchecked)
            item.setData(QVariant(serie))
            model.appendRow(item)
        model.itemChanged.connect(self.__serieStateChanged)
        model.sort(0)
        
        # update the model of the list view
        self.__ui.dataSeriesListView.setModel(model)

        # use configuration's data format
        self.__ui.formatSelection.setFormat(config.getFormat())

        # use configuration's scale
        self.__ui.scaleSelection.setScale(config.getScale())

    def getConfiguration(self):
        return self.__config


        
