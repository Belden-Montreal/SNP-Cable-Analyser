from snpanalyzer.gui.ui.cable_configuration import Ui_form
from snpanalyzer.sample.port import EthernetPair

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QDialogButtonBox

class CableConfigurationDialog(QDialog):
    def __init__(self, config=None):
        super(CableConfigurationDialog, self).__init__()
        self.__config = config
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # setup the combo boxes
        self.__selections = dict()
        self.__groups = {i: set() for i in range(8)}
        self.__conflicts = set()
        self.__setupComboBox(self.__ui.inputPort1ComboBox,  default=0)
        self.__setupComboBox(self.__ui.inputPort2ComboBox,  default=1)
        self.__setupComboBox(self.__ui.inputPort3ComboBox,  default=2)
        self.__setupComboBox(self.__ui.inputPort4ComboBox,  default=3)
        self.__setupComboBox(self.__ui.outputPort1ComboBox, default=4)
        self.__setupComboBox(self.__ui.outputPort2ComboBox, default=5)
        self.__setupComboBox(self.__ui.outputPort3ComboBox, default=6)
        self.__setupComboBox(self.__ui.outputPort4ComboBox, default=7)

        # setup pair 12
        self.__setupPair(
            EthernetPair.PAIR12,
            self.__ui.pair12NameEdit,
            self.__ui.inputPort1LineEdit,
            self.__ui.inputPort1ComboBox,
            self.__ui.outputPort1LineEdit,
            self.__ui.outputPort1ComboBox
        )

        # setup pair 36
        self.__setupPair(
            EthernetPair.PAIR36,
            self.__ui.pair36NameEdit,
            self.__ui.inputPort2LineEdit,
            self.__ui.inputPort2ComboBox,
            self.__ui.outputPort2LineEdit,
            self.__ui.outputPort2ComboBox
        )

        # setup pair 45
        self.__setupPair(
            EthernetPair.PAIR45,
            self.__ui.pair45NameEdit,
            self.__ui.inputPort3LineEdit,
            self.__ui.inputPort3ComboBox,
            self.__ui.outputPort3LineEdit,
            self.__ui.outputPort3ComboBox
        )

        # setup pair 78
        self.__setupPair(
            EthernetPair.PAIR78,
            self.__ui.pair78NameEdit,
            self.__ui.inputPort4LineEdit,
            self.__ui.inputPort4ComboBox,
            self.__ui.outputPort4LineEdit,
            self.__ui.outputPort4ComboBox
        )

        # button signals
        self.__ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.__ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.reject)

        # setup check box
        self.__setupCheckBox()

    def __setupComboBox(self, box, default=0):
        # align text to center
        box.setEditable(True)
        box.lineEdit().setReadOnly(True)
        box.lineEdit().setAlignment(Qt.AlignCenter)

        # add possible ports
        for i in range(8):
            box.addItem("Port {}".format(i+1), userData = i)

        # select the default selection
        box.setCurrentIndex(default)
        self.__setComboBox(box, default)

        # activate index changed signal
        box.currentIndexChanged.connect(lambda index: self.__setComboBox(box, index))

    def __setupCheckBox(self):
        # checkbox signal
        self.__ui.hideNamesCheckBox.stateChanged.connect(self.__hideNames)

        # checked by default
        self.__ui.hideNamesCheckBox.setCheckState(Qt.Checked)

    def __setupPair(self, pair, pairName, mainName, mainBox, remoteName, remoteBox):
        # get the pair
        wire = self.__config.getByType(pair)
        if wire is None:
            return

        # set the pair name
        pairName.setText(wire.getName())

        # setup the main port
        mainName.setText(wire.getMainPort().getName())
        self.__setComboBox(mainBox, wire.getMainPort().getIndex())

        # setup the remote port
        remoteName.setText(wire.getRemotePort().getName())
        self.__setComboBox(remoteBox, wire.getRemotePort().getIndex())

    def __setComboBox(self, box, index):
        # remove box from his index
        if box in self.__selections:
            old = self.__selections[box]
            self.__groups[old].discard(box)
            self.__highlightBoxes(old)

        # add the box to the new index
        self.__groups[index].add(box)
        self.__highlightBoxes(index)

        # set the index
        self.__selections[box] = index

    def __highlightBoxes(self, index):
        # get the group of port with this index
        group = self.__groups[index]

        # check if multiple ports has the same index
        if len(group) == 1:
            {box.setStyleSheet('color: black;') for box in group}
            self.__conflicts.discard(index)
        else:
            {box.setStyleSheet('color: red;') for box in group}
            self.__conflicts.add(index)

        # disable confirmation button if needed
        if len(self.__conflicts):
            self.__ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.__ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def __hideNames(self, state):
        hide = True if state == Qt.Checked else False

        self.__ui.pair12NameEdit.setHidden(hide)           
        self.__ui.pair36NameEdit.setHidden(hide)
        self.__ui.pair45NameEdit.setHidden(hide)
        self.__ui.pair78NameEdit.setHidden(hide)

        self.__ui.inputPort1LineEdit.setHidden(hide)
        self.__ui.inputPort2LineEdit.setHidden(hide)
        self.__ui.inputPort3LineEdit.setHidden(hide)
        self.__ui.inputPort4LineEdit.setHidden(hide)

        self.__ui.outputPort1LineEdit.setHidden(hide)
        self.__ui.outputPort2LineEdit.setHidden(hide)
        self.__ui.outputPort3LineEdit.setHidden(hide)
        self.__ui.outputPort4LineEdit.setHidden(hide)

    def getConfiguration(self):
        # TODO: generate the configuration from the settings
        return self.__config
