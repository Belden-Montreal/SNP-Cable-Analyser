from gui.ui.export.sample import Ui_form

from PyQt5.QtCore import Qt, QVariant, QItemSelectionModel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class ExportSampleWidget(QWidget):
    def __init__(self, parent=None):
        super(ExportSampleWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # setup config
        self.__config    = None
        self.__model     = None
        self.__parameter = None

    def __parameterStateChanged(self, item):
        # get the paramete serie from the checked item
        ptype = item.data()

        # add/remove the parameter from the configuration
        if item.checkState() == Qt.Checked:
            self.__config.addParameter(ptype)
        else:
            self.__config.removeParameter(ptype)

        # disable the widget if the we do not export this parameter
        widgetConfig = self.__ui.parameterExportWidget.getConfiguration()
        if widgetConfig is not None:
            self.__ui.parameterExportWidget.setEnabled(widgetConfig.doExport())

    def __parameterSelectionChanged(self, current, previous):
        # make sure a model is setup
        if self.__model is None:
            return

        # get the parameter
        ptype = self.__model.itemFromIndex(current).data()
        if ptype == self.__parameter:
            return
        self.__parameter = ptype

        # get the configuration
        config = self.__config.getParameters()[ptype]

        # change the configuration in the widget
        self.__ui.parameterExportWidget.setExportConfiguration(config)

        # disable the widget if the we do not export this parameter
        self.__ui.parameterExportWidget.setEnabled(config.doExport())

    def setExportConfiguration(self, config):
        # change configuration
        self.__config = config

        # remove selection signals
        if self.__ui.parametersListView.selectionModel() is not None:
            self.__ui.parametersListView.selectionModel().currentChanged.disconnect()

        # create the new model
        model = QStandardItemModel()
        for (ptype, export) in config.getParameters().items():
            item = QStandardItem()
            item.setText(export.getParameter().getName())
            item.setCheckable(True)
            item.setCheckState(Qt.Checked if export.doExport() else Qt.Unchecked)
            item.setData(QVariant(ptype))
            model.appendRow(item)
        model.itemChanged.connect(self.__parameterStateChanged)
        model.sort(0)
        
        # update the model of the list view
        self.__ui.parametersListView.setModel(model)
        self.__model = model

        # update selection signal
        self.__ui.parametersListView.selectionModel().currentChanged.connect(
            self.__parameterSelectionChanged
        )

    def getConfiguration(self):
        return self.__config


        
