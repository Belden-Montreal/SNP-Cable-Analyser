from snpanalyzer.gui.ui.vna_configuration import Ui_form
from snpanalyzer.config.vna import VNAConfiguration

from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

class VNAConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super(VNAConfigurationWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # restrict to numbers
        self.__ui.resolutionLineEdit.setValidator(QIntValidator())
        self.__ui.averageLineEdit.setValidator(QIntValidator())
        self.__ui.portsLineEdit.setValidator(QIntValidator())
        self.__ui.timeoutLineEdit.setValidator(QIntValidator())

        # use default VNA configuration
        self.setConfiguration(VNAConfiguration())

        # connect signals
        self.__ui.addressLineEdit.textChanged.connect(self.__setAddress)
        self.__ui.bandwidthInput.changed.connect(self.__setBandwidth)
        self.__ui.startFreqInput.changed.connect(self.__setStartFreq)
        self.__ui.stopFreqInput.changed.connect(self.__setStopFreq)
        self.__ui.resolutionLineEdit.textChanged.connect(self.__setResolution)
        self.__ui.averageLineEdit.textChanged.connect(self.__setAverage)
        self.__ui.portsLineEdit.textChanged.connect(self.__setPorts)
        self.__ui.timeoutLineEdit.textChanged.connect(self.__setTimeout)

    def setConfiguration(self, vna):
        self.__vna = vna
        self.__ui.addressLineEdit.setText(vna.getAddress())
        self.__ui.bandwidthInput.setValue(vna.getBandwidth())
        self.__ui.startFreqInput.setValue(vna.getMinimumFrequency())
        self.__ui.stopFreqInput.setValue(vna.getMaximumFrequency())
        self.__ui.resolutionLineEdit.setText(str(vna.getResolution()))
        self.__ui.averageLineEdit.setText(str(vna.getAverage()))
        self.__ui.portsLineEdit.setText(str(vna.getNumberOfPorts()))
        self.__ui.timeoutLineEdit.setText(str(vna.getTimeout()))

    def getConfiguration(self):
        return self.__vna

    def __setAddress(self, address):
        self.__vna.setAddress(address)
        if self.__vna.getAddress() != address:
            self.__ui.addressLineEdit.setText(self.getAddress())

    def __setBandwidth(self, bandwidth):
        self.__vna.setBandwidth(bandwidth)
        if self.__vna.getBandwidth() != bandwidth:
            self.__ui.bandwithInput.setValue(self.__vna.getBandwidth())

    def __setStartFreq(self, freq):
        self.__vna.setMinimumFrequency(freq)
        if self.__vna.getMinimumFrequency() != freq:
            self.__ui.startFreqInput.setValue(self.__vna.getMinimumFrequency())

    def __setStopFreq(self, freq):
        self.__vna.setMaximumFrequency(freq)
        if self.__vna.getMaximumFrequency() != freq:
            self.__ui.stopFreqInput.setValue(self.__vna.getMaximumFrequency())

    def __setResolution(self, resolution):
        try:
            resolution = int(resolution)
        except:
            resolution = -1
        self.__vna.setResolution(resolution)
        if self.__vna.getResolution() != resolution:
            self.__ui.resolutionLineEdit.setText(str(self.__vna.getResolution()))

    def __setAverage(self, average):
        try:
            average = int(average)
        except:
            average = -1
        self.__vna.setAverage(average)
        if self.__vna.getAverage() != average:
            self.__ui.averageLineEdit.setText(str(self.__vna.getAverage()))

    def __setPorts(self, ports):
        try:
            ports = int(ports)
        except:
            ports = -1
        self.__vna.setNumberOfPorts(ports)
        if self.__vna.getNumberOfPorts() != ports:
            self.__ui.portsLineEdit.setText(str(self.__vna.getNumberOfPorts()))

    def __setTimeout(self, timeout):
        try:
            timeout = int(timeout)
        except:
            timeout = -1
        self.__vna.setTimeout(timeout)
        if self.__vna.getTimeout() != timeout:
            self.__ui.timeoutLineEdit.setText(str(self.__vna.getTimeout()))

