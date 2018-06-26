import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import MW4
import MainWidget
import new_project_dialog
from ParameterWidget import ParameterWidget
from app.project_manager import ProjectManager
from app.import_dialog import ImportSNPDialog
from app.vna_manager import VNAManager
from limits.LimitDialog import LimitDialog

class Main():

    def __init__(self):
        self._qmw = QtWidgets.QMainWindow()
        self._mainWindow = MW4.Ui_MainWindow()

        self._mainWindow.setupUi(self._qmw)
        self._mainWindow.sampleTable.setColumnCount(2)
        self._mainWindow.sampleTable.setHorizontalHeaderLabels(["Name","Date"])
        self._mainWindow.sampleTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._mainWindow.sampleTable.customContextMenuRequested.connect(lambda pos:self.tableContextMenu(pos))
        self._selected = list()
        self._projectManager = ProjectManager()
        self._mainWindow.actionToolbar_Import_SnP.setDisabled(True)
        self._mainWindow.actionImport_SnP.setDisabled(True)
        self._vnaManager = VNAManager()

        #Here, we process any arguments that might be sent the program from outside of the interface.
        #In other words, when ever a user right click on an SNP files, rather than opening them in Notepad, it would be opened in this interface.
        arguments = sys.argv[1:] 
        
        if len(arguments):
            print(arguments)
            #TODO: load a project from file

        self._mainWindow.actionToolbar_Import_SnP.triggered.connect(lambda:self.importSNP())
        self._mainWindow.actionNew_Project.triggered.connect(lambda:self.newProject())
        self._mainWindow.sampleTable.itemSelectionChanged.connect(lambda:self.setActiveSample())
        self._mainWindow.actionRun.triggered.connect(lambda:self._vnaManager.acquire())
        self._mainWindow.actionImport_SnP.triggered.connect(lambda:self._vnaManager.acquire())
        self._mainWindow.actionConnect.triggered.connect(lambda:self._vnaManager.connect())
        self._mainWindow.actionWho_am_I.triggered.connect(lambda:self._vnaManager.whoAmI())
        # self.actionMeasure.triggered.connect(MainWindow.aquire)
        self._mainWindow.actionCalibrate_2.triggered.connect(lambda:self._vnaManager.calibrate())
        self._mainWindow.actionDisconnect.triggered.connect(lambda:self._vnaManager.disconnect())
        # self.actionAlien.triggered.connect(MainWindow.addAlien)
        # self.actionDeembed.triggered.connect(MainWindow.addEmbed)
        # self.param_tabs.currentChanged['int'].connect(MainWindow.tabChange)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def updateSamplesTable(self):
        project = self._projectManager.activeProject()
        num = project.numSamples()
        self._mainWindow.sampleTable.setRowCount(num)
        for i in range(num):
            print(project.samples()[i].getName())
            self._mainWindow.sampleTable.setItem(i, 0, QtWidgets.QTableWidgetItem(project.samples()[i].getName()))
            self._mainWindow.sampleTable.setItem(i, 1, QtWidgets.QTableWidgetItem(project.samples()[i].getDate()))
        self._mainWindow.sampleTable.resizeColumnsToContents()


    def newProject(self):
        dialog = QtWidgets.QDialog(self._qmw)
        newDial = new_project_dialog.Ui_NewProjectDialog()
        newDial.setupUi(dialog)
        projectTypes = ["Alien", "Plug", "Embedding", "Other"]
        newDial.typeBox.addItems(projectTypes)
        res = dialog.exec_()
        if res:
            projType = newDial.typeBox.currentText()
            projName = newDial.nameEdit.text()
            if projType == "Alien":
                self._projectManager.newAlienProject(projName)
            elif projType == "Plug":
                self._projectManager.newPlugProject(projName)
            elif projType == "Embedding":
                self._projectManager.newEmbeddingProject(projName)
            else:
                self._projectManager.newProject(projName)
            self._mainWindow.actionToolbar_Import_SnP.setDisabled(False)
            self._mainWindow.actionImport_SnP.setDisabled(False)
            self._qmw.setWindowTitle("Belden Network Analyzer Software - "+projName)

    def importSNP(self):
        self._projectManager.importFiles(self._qmw)
        self.updateSamplesTable()

    def setActiveSample(self):
        self._selected = list()
        for i in self._mainWindow.sampleTable.selectionModel().selectedRows():
            self._selected.append(self._mainWindow.sampleTable.item(i.row(), 0).text())
        
        if len(self._selected) == 1:
            self.displaySampleParams(self._selected[0])

    def displaySampleParams(self, sampleName):
        if not sampleName:
            self._mainWindow.param_tabs.clear()
            return
        
        self._mainWindow.param_tabs.clear()
        sample = self._projectManager.activeProject().findSamplesByName([sampleName])[0]
        mainTab = QtWidgets.QWidget()
        mainTabWidget = MainWidget.Ui_MainWidget()
        mainTabWidget.setupUi(mainTab)
        self._mainWindow.param_tabs.addTab(mainTab, "Main")

        for name, param in sample.getParameters().items():
            newTab = ParameterWidget(name, param)
            self._mainWindow.param_tabs.addTab(newTab.widget, name)

    def tableContextMenu(self, pos):
        if len(self._selected) > 0 and self._projectManager.activeProject():

            menu = QtWidgets.QMenu()
            setLimit = menu.addAction("Set Limit")

            if len(self._selected) == 1: 
                setPortNumber = menu.addAction("Renumber Ports")

            exportExcel = menu.addAction("Export To Excel")
            delete = menu.addAction("Delete")

            action = menu.exec_(QtGui.QCursor.pos())

            if action == exportExcel:
                print(self._selected)
                file, _ = QtWidgets.getSaveFileName(self,"Export Excel Repport", "","Excel File (*.xlsx)")
                self._projectManager.activeProject().generateExcel(file , self._selected, True)

            elif action == delete:
                self._projectManager.activeProject().removeSamples(self._selected)

            elif action == setLimit:
                self.setLimit()
            #self.Project.activeMeasurements = selected

            # elif action == setPortNumber and len(self._selected) == 1:
            #     self.setPortNumber()
            return 1

        menu = QtWidgets.QMenu()
        addSNP = menu.addAction("Add Sample")
        selectAll = menu.addAction("Select All")
        action = menu.exec_(QtGui.QCursor.pos())
        if action == selectAll:
            self._mainWindow.sampleTable.selectAll()
        elif action == addSNP:
            self.importSNP()

    def setLimit(self):
        
        limitDialog = LimitDialog()
        result = limitDialog.showDialog()
        if result:
            item = limitDialog.getSelection().internalPointer().standard
            project = self._projectManager.activeProject()
            for sample in self._selected:
                project.findSamplesByName(sample)[0].setStandard(item)
                for i in range(project.numSamples()):
                    if self._mainWindow.sampleTable.item(i,0).text() == sample:
                        self._mainWindow.sampleTable.setItem(i, 2, QtWidgets.QTableWidgetItem(item.name))
            self._mainWindow.sampleTable.resizeColumnsToContents()
            self.displaySampleParams(self._selected[0])
    
    def showMaximized(self):
        self._qmw.showMaximized()


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    app.setStyle('fusion')
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    #pixmap = QtGui.QPixmap("splash.jpeg")
    #splash = QtWidgets.QSplashScreen(pixmap)
    #splash.show()

    #time.sleep(10)
    form = Main()  # We set the  form to be our ExampleApp (design)

    #form.show()  # Show the form
    form.showMaximized()

    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    #splash.finish(form)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()