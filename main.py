import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import MW4
import MainWidget
import new_project_dialog
from ParameterWidget import ParameterWidget
from app.project_manager import ProjectManager
from app.vna_manager import VNAManager
from app.tree_model import TreeModel
from limits.LimitDialog import LimitDialog
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Main():

    def __init__(self):
        self._qmw = QtWidgets.QMainWindow()
        self._mainWindow = MW4.Ui_MainWindow()

        self._mainWindow.setupUi(self._qmw)
        #self._mainWindow.sampleTable.setColumnCount(2)
        #self._mainWindow.sampleTable.setHeaderLabels(["Name","Date"])
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
        self._vnaManager = VNAManager()

        nav = NavigationToolbar(self._mainWindow.graphicsView, self._qmw)
        self._mainWindow.verticalLayout_3.addWidget(nav)
        #Here, we process any arguments that might be sent the program from outside of the interface.
        #In other words, when ever a user right click on an SNP files, rather than opening them in Notepad, it would be opened in this interface.
        arguments = sys.argv[1:] 
        
        if len(arguments):
            print(arguments)
            #TODO: load a project from file

        self._mainWindow.actionToolbar_Import_SnP.triggered.connect(lambda:self.importSNP())
        self._mainWindow.actionNew_Project.triggered.connect(lambda:self.newProject())
        self._mainWindow.sampleTable.clicked.connect(lambda:self.setActiveSample())
        self._mainWindow.actionRun.triggered.connect(lambda:self._vnaManager.acquire())
        self._mainWindow.actionImport_SnP.triggered.connect(lambda:self._vnaManager.acquire())
        self._mainWindow.actionConnect.triggered.connect(lambda:self._vnaManager.connect())
        self._mainWindow.actionWho_am_I.triggered.connect(lambda:self._vnaManager.whoAmI())
        # self.actionMeasure.triggered.connect(MainWindow.aquire)
        self._mainWindow.actionCalibrate_2.triggered.connect(lambda:self._vnaManager.calibrate())
        self._mainWindow.actionDisconnect.triggered.connect(lambda:self._vnaManager.disconnect())
        # self.actionAlien.triggered.connect(MainWindow.addAlien)
        # self.actionDeembed.triggered.connect(MainWindow.addEmbed)
        self._mainWindow.param_tabs.currentChanged['int'].connect(lambda:self.tabChanged())
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self._mainWindow.actionImport_Project.triggered.connect(lambda: self.loadProject())
        self._mainWindow.actionSave_Project.triggered.connect(lambda: self.saveProject())

    def getRootProject(self):
         selecteds = self.getSelected()
         if len(selecteds) > 0:
            selected = selecteds[0]
            while self._model.parent(selected) != QtCore.QModelIndex():
                selected = self._model.parent(selected)
            return selected.internalPointer().getObject()
             

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
                node = self._projectManager.newAlienProject(projName)
            elif projType == "Plug":
                node = self._projectManager.newPlugProject(projName)
            elif projType == "Embedding":
                node = self._projectManager.newEmbeddingProject(projName)
            else:
                node = self._projectManager.newProject(projName)
            self._model.beginResetModel()
            self._model.rootItem.addChild(node)
            self._model.endResetModel()
            self._mainWindow.actionToolbar_Import_SnP.setDisabled(False)
            self._mainWindow.actionImport_SnP.setDisabled(False)

    def importSNP(self):
        self._model.beginResetModel()
        self._model.getRootFromIndex(self.getSelected()[0]).internalPointer().openImportWindow(self._qmw)
        self._model.endResetModel()

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
        sample = index.internalPointer().getObject()
        try:
            mainTab = self.setupMainTab(sample)
        except:
            return #TODO: handle selections of projects/subprojects with showData()
        failParams = list()
        for name, param in sample.getParameters().items():
            try:
                if param.visible():
                    newTab = ParameterWidget(name, param)
                    self._mainWindow.param_tabs.addTab(newTab, name)
                    if not newTab.hasPassed:
                        failParams.append(name)
            except:
                continue
        if len(failParams) > 0:
            mainTab.passLabel.setText("Fail")
        else:
            mainTab.passLabel.setText("Pass")
        mainTab.failsLabel.setText(str(failParams))

    def setupMainTab(self, sample):
        mainTab = QtWidgets.QWidget()
        mainTabWidget = MainWidget.Ui_MainWidget()
        mainTabWidget.setupUi(mainTab)
        mainTabWidget.testNameLabel.setText(sample.getName()+":")
        mainTabWidget.dateLabel.setText(sample.getDate())
        mainTabWidget.limitLabel.setText(str(sample.getStandard()))
        self._mainWindow.param_tabs.addTab(mainTab, "Main")
        return mainTabWidget

    def tableContextMenu(self, pos):
        selectedProj = self.getRootProject()
        selected = self.getSelected()
        if selectedProj and len(selected) > 0:
    
            menu = QtWidgets.QMenu()
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
                    selectedProj.generateExcel(file , selected[0], z)

            elif action == delete:
                self._model.beginResetModel()
                for s in selected:
                    s.internalPointer().delete()
                self._model.endResetModel()
                
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
            selected = [x.text(0) for x in self.getSelected()]
            project = self.getRootProject()
            for sample in selected:
                project.findSamplesByName(sample)[0].setStandard(item)
            self.displaySampleParams(selected[0])

    def tabChanged(self):
        if self._mainWindow.param_tabs.currentIndex() == 0 or self._mainWindow.param_tabs.count() <= 1:
            self._mainWindow.graphicsView.setVisible(False)
            return
        self._mainWindow.graphicsView.setVisible(True)
        parameter = self._mainWindow.param_tabs.currentWidget().parameter
        plot = parameter.getPlot()
        self._mainWindow.graphicsView.figure = plot.getFigure()
        self._mainWindow.graphicsView.draw() 

    def loadProject(self):
        f, ok = QtWidgets.QFileDialog.getOpenFileName(self._qmw, caption="Load a project", directory="projects/", filter="Belden Network Analyzer Project file (*.bnap)")
        if ok:
            self._model.beginResetModel()
            self._projectManager.loadProject(f)
            self._model.endResetModel()
            self._mainWindow.actionToolbar_Import_SnP.setDisabled(False)
            self._mainWindow.actionImport_SnP.setDisabled(False)

    def saveProject(self):
        f, ok = QtWidgets.QFileDialog.getSaveFileName(self._qmw, caption="Save project", directory="projects/", filter="Belden Network Analyzer Project file (*.bnap)")
        if ok:
            self._projectManager.saveProject(f, self.getRootProject())

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