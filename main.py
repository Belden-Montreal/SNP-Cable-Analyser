import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from snpanalyzer.gui.ui import MW
from snpanalyzer.gui.ui import new_project_dialog
from snpanalyzer.app.project_manager import ProjectManager
from snpanalyzer.vna import VNA
from snpanalyzer.app.tree_model import TreeModel
from snpanalyzer.gui.dialog.vna_test import VNATestDialog
from snpanalyzer.gui.dialog.LimitDialog import LimitDialog
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from snpanalyzer.export.project import ProjectExportConfiguration
from snpanalyzer.gui.dialog.export_configuration import ExportConfigurationDialog
from pathlib import Path

class Main():

    def __init__(self):
        self._qmw = QtWidgets.QMainWindow()
        self._mainWindow = MW.Ui_MainWindow()

        self._mainWindow.setupUi(self._qmw)
        self._model = TreeModel()
        self._mainWindow.sampleTable.setModel(self._model)
        self._mainWindow.sampleTable.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._mainWindow.sampleTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._mainWindow.sampleTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._mainWindow.sampleTable.customContextMenuRequested.connect(lambda pos:self.tableContextMenu(pos))
        self._selected = list()
        self._projectManager = ProjectManager()
        self._mainWindow.actionToolbar_Import_SnP.setDisabled(True)
        self._mainWindow.actionImport_SnP.setDisabled(True)
        self._vnaManager = VNA()
        self.activeNode = None

        #Here, we process any arguments that might be sent the program from outside of the interface.
        #In other words, when ever a user right click on an SNP files, rather than opening them in Notepad, it would be opened in this interface.
        arguments = sys.argv[1:] 
        
        if len(arguments):
            print(arguments)
            #TODO: load a project from file

        self._mainWindow.actionToolbar_Import_SnP.triggered.connect(lambda:self.importSNP())
        self._mainWindow.actionNew_Project.triggered.connect(lambda:self.newProject())
        self._mainWindow.sampleTable.clicked.connect(lambda:self.setActiveSample())
        self._mainWindow.actionRun.triggered.connect(lambda:self.acquire())
        self._mainWindow.actionConnect.triggered.connect(lambda:self.connect())
        self._mainWindow.actionWho_am_I.triggered.connect(lambda:self._vnaManager.whoAmI())
        self._mainWindow.actionMeasure.triggered.connect(lambda:self.acquire())
        self._mainWindow.actionCalibrate_2.triggered.connect(lambda:self._vnaManager.calibrate())
        self._mainWindow.actionDisconnect.triggered.connect(lambda:self.disconnect())
        self._mainWindow.actionAlien.triggered.connect(lambda:self.newProject(0))
        self._mainWindow.actionDeembed.triggered.connect(lambda:self.newProject(2))
        self._mainWindow.actionImport_Project.triggered.connect(lambda: self.loadProject())
        self._mainWindow.actionSave_Project.triggered.connect(lambda: self.saveProject())
        self._mainWindow.actionExport_PDF.triggered.connect(lambda: self.exportPDF())
        self._mainWindow.param_tabs.currentChanged.connect(lambda: self.tabChanged())


    def acquire(self):
        print(self.getRootProject())
        try:
            vnaDialog = VNATestDialog()
            vnaDialog.exec_()
            name = vnaDialog.getSampleName()
            ports = vnaDialog.getPorts()
            sample_file = self._vnaManager.acquire(name, ports)
            self.getRootProject().addSamples([sample_file])
        except Exception as e:
            print(e)
        
    def connect(self):
        self._vnaManager.connect()
        if self._vnaManager.connected():
            self._mainWindow.actionMeasure.setEnabled(True)
            self._mainWindow.actionWho_am_I.setEnabled(True)
            self._mainWindow.actionCalibrate.setEnabled(True)
            self._mainWindow.actionCalibrate_2.setEnabled(True)
            self._mainWindow.actionDisconnect.setEnabled(True)
            self._mainWindow.actionRun.setEnabled(True)
            self._mainWindow.actionConnect.setEnabled(False)
            
    def disconnect(self):
        self._vnaManager.disconnect()
        self._mainWindow.actionMeasure.setEnabled(False)
        self._mainWindow.actionWho_am_I.setEnabled(False)
        self._mainWindow.actionCalibrate.setEnabled(False)
        self._mainWindow.actionCalibrate_2.setEnabled(False)
        self._mainWindow.actionDisconnect.setEnabled(False)
        self._mainWindow.actionRun.setEnabled(False)
        self._mainWindow.actionConnect.setEnabled(True)

    def getRootProject(self):
         selected = self.getSelected()
         if len(selected) > 0:
            return self._model.itemFromIndex(self._model.getRootFromIndex(selected[0]))
             

    def newProject(self, first=3):
        dialog = QtWidgets.QDialog(self._qmw)
        newDial = new_project_dialog.Ui_NewProjectDialog()
        newDial.setupUi(dialog)
        projectTypes = ["Alien", "Plug", "Embedding", "Other"]
        newDial.typeBox.addItems(projectTypes)
        newDial.typeBox.setCurrentIndex(first)
        res = dialog.exec_()
        if res:
            projType = newDial.typeBox.currentText()
            projName = newDial.nameEdit.text()
            if projType == "Alien":
                node = self._projectManager.newAlienProject(projName)
            elif projType == "Plug":
                node = self._projectManager.newPlugProject(projName)
            elif projType == "Embedding":
                node = self._projectManager.newEmbeddingProject(projName)
            else:
                node = self._projectManager.newProject(projName)
            self._model.appendRow(node)
            self._mainWindow.actionToolbar_Import_SnP.setDisabled(False)
            self._mainWindow.actionImport_SnP.setDisabled(False)

    def importSNP(self):
        self.getRootProject().openImportWindow(self._qmw)

    def getSelected(self):
        return self._mainWindow.sampleTable.selectionModel().selectedRows()

    def setActiveSample(self):
        selected = self.getSelected()
        
        if len(selected) == 1:
            self.displaySampleParams(selected[0])

    def displaySampleParams(self, index):
        if not index:
            self._mainWindow.param_tabs.clear()
            return
        
        self._mainWindow.param_tabs.clear()
        node = self._model.itemFromIndex(index)
        self.activeNode = node
        #if "ProjectNode" not in str(type(node)):
        #    node._dataObject.createAnalyses()
        tabs = node.getWidgets(self._vnaManager)
        for name, tab in tabs.items():
            self._mainWindow.param_tabs.addTab(tab, name)

    def tabChanged(self):
        # if self._mainWindow.param_tabs.currentIndex() == 0 or self._mainWindow.param_tabs.count() <= 1:
        #      self._mainWindow.graphicsView.setVisible(False)
        #      return
        # self._mainWindow.graphicsView.setVisible(True)
        # parameter = self._mainWindow.param_tabs.currentWidget().parameter
        # plot = parameter.getPlot()
        # currentTab = self._mainWindow.param_tabs.currentWidget()
        # if currentTab:
        #     currentTab.showTab()
        self.tab_index = self._mainWindow.param_tabs.currentIndex()
        self.activeParameter = self._mainWindow.param_tabs.tabText(self.tab_index)
        print(self.activeParameter)
        if "ProjectNode" not in str(type(self.activeNode )):
            try:
                print("Created")
                self.activeNode._dataObject.createAnalyses(desiredParam = self.activeParameter)
                self._mainWindow.param_tabs.currentWidget().setGraphic(self.activeNode._dataObject.getAnalysis(self.activeParameter))
                print("Creating Graphic")
            except Exception as e:
                print(e)
        if self._mainWindow.param_tabs.currentIndex() == 0 or self._mainWindow.param_tabs.count() <= 1:
            #self._mainWindow.graphicsView.setVisible(False)
            print("Tab Changed")
            return

    def tableContextMenu(self, pos):
        selected = self.getSelected()
        if self.getRootProject():
            selectedProj = self.getRootProject().getObject()
        else:
            selectedProj = None
        if selectedProj and len(selected) > 0:
    
            menu = QtWidgets.QMenu()
            addSample = menu.addAction("Add Samples")
            setLimit = menu.addAction("Set Limit")

            if len(selected) == 1: 
                setPortNumber = menu.addAction("Renumber Ports")

            exportExcel = menu.addAction("Export To Excel")
            delete = menu.addAction("Delete")

            action = menu.exec_(QtGui.QCursor.pos())

            if action == exportExcel:
                res, ok = QtWidgets.QInputDialog.getItem(self._qmw, "Select the Data type", "Data Type", ["Complex", "magnitude/phase"], editable=False)
                if ok:
                    if res == "Complex":
                        z = True
                    else:
                        z = False
                    file, _ = QtWidgets.QFileDialog.getSaveFileName(self._qmw,"Export Excel Report", "","Excel File (*.xlsx)")
                    selected_samples = []
                    for s in selected:
                        s = self._model.itemFromIndex(s).getObject()
                        if(type(s.getSamples()) is list):  
                            selected_samples.extend(s.getSamples())
                        else:
                            selected_samples.append(s.getSamples())
                    print(selected_samples)
                    try:
                        for x in selected_samples:
                            print("Here : "+ x.getName())
        
                        #print([self._model.itemFromIndex(s).getObject().getSamples().getName() for s in selected])
                        selectedProj.generateExcel(file, [s.getName() for s in selected_samples], z)
                    except Exception as e:
                        errorMessage = QtWidgets.QErrorMessage(self._qmw)
                        errorMessage.showMessage(str(e))


            elif action == delete:
                sel = [self._model.itemFromIndex(s) for s in selected]
                for s in sel:
                    s.delete()

            elif action == setLimit:
                self.setLimit()

            elif action == addSample:
                self.importSNP()
            #self.Project.activeMeasurements = selected

            # elif action == setPortNumber and len(self._selected) == 1:
            #     self.setPortNumber()
            return 1

        menu = QtWidgets.QMenu()
        addSNP = menu.addAction("Add Project")
        selectAll = menu.addAction("Select All")
        action = menu.exec_(QtGui.QCursor.pos())
        if action == selectAll:
            self._mainWindow.sampleTable.selectAll()
        elif action == addSNP:
            self.newProject()

    def exportPDF(self):
        selected = self.getSelected()
        if self.getRootProject():
            selectedProj = self.getRootProject().getObject()
        else:
            selectedProj = None
        if selectedProj and len(selected) > 0:
            config = ProjectExportConfiguration(selectedProj)
            dialog = ExportConfigurationDialog(config)
            #.show()
            dialog.exec_()
            obj = config.generateDocumentObject(
                dialog.getTemporaryDirectory(),
                Path("")
            )
            obj.compile(filename=dialog.getDocumentFilename())
    
    def setLimit(self):
        
        limitDialog = LimitDialog()
        result = limitDialog.showDialog()
        if result:
            item = limitDialog.getSelection().internalPointer().standard
            selected = [self._model.itemFromIndex(x) for x in self.getSelected()]
            for node in selected:
                node.setStandard(item)
            self.displaySampleParams(self.getSelected()[0])



    def loadProject(self):
        f, ok = QtWidgets.QFileDialog.getOpenFileName(self._qmw, caption="Load a project", directory="projects/", filter="Belden Network Analyzer Project file (*.bnap)")
        if ok:
            node = self._projectManager.loadProject(f)
            self._model.appendRow(node)
            self._mainWindow.actionToolbar_Import_SnP.setDisabled(False)
            self._mainWindow.actionImport_SnP.setDisabled(False)

    def saveProject(self):
        f, ok = QtWidgets.QFileDialog.getSaveFileName(self._qmw, caption="Save project", directory="projects/", filter="Belden Network Analyzer Project file (*.bnap)")
        if ok:
            self._projectManager.saveProject(f, self.getRootProject().getObject())

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
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    #splash.finish(form)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
