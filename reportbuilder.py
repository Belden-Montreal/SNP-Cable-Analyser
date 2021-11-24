
class ReportBuilder():

    def __init__(self, samples):

        def self.samples = samples

    def configReportUI(self):
        for l in self.alienSample.vic_port_names:
            chkBoxItem = QListWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setText(l)
            chkBoxItem.setCheckState(QtCore.Qt.CheckState.Checked)
            #checkbox = QCheckBox(label, self.paramWidget.resultsList)
            #checkbox.setChecked(True)  

            self.alienWidget.plotList.addItem(chkBoxItem)
        