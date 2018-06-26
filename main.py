import sys
from PyQt5 import QtWidgets, QtCore
import MW4
import new_project_dialog
from app.project_manager import ProjectManager
from app.import_dialog import ImportSNPDialog
from app.vna_manager import VNAManager

class Main():

    def __init__(self):
        self._qmw = QtWidgets.QMainWindow()
        self._mainWindow = MW4.Ui_MainWindow()

        self._mainWindow.setupUi(self._qmw)
        self._mainWindow.sampleTable.setColumnCount(2)
        self._mainWindow.sampleTable.setHorizontalHeaderLabels(["Name","Date"])
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
        # self.sampleTable.itemSelectionChanged.connect(MainWindow.setActiveSample)
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