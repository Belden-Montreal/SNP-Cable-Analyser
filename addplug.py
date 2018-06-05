from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import scipy
import plugDialog
import VNA_addr_dialog
import TestParameters
from Communication import Communication
import matplotlib.figure
import matplotlib.backends.backend_qt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.pyplot import cm

import numpy as np

from embedding2 import Embedding


class AddPlug(QtWidgets.QMainWindow, plugDialog.Ui_Dialog, QtWidgets.QAction, QtWidgets.QFileDialog, QtWidgets.QListView, QtWidgets.QDialog, QtCore.Qt):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)

        self.em = Embedding()

        self.dfOpen = None
        self.dfShort = None
        self.pdfOpen = None
        self.pdfShort = None
        self.pdfLoad = None

        font = QtGui.QFont()
        font.setPointSize(7)
        self.df_open_label.setFont(font)
        self.df_short_label.setFont(font)
        self.pdf_open_label.setFont(font)
        self.pdf_short_label.setFont(font)
        self.pdf_load_label.setFont(font)
        '''Here we will connect the buttons (import/acquire) to their apropriate functions'''

        self.df_open_import.clicked.connect(self.dfOpenImport)
        #self.df_open_acquire.clicked.connect(self.dfOpenAcquire)
        self.df_short_import.clicked.connect(self.dfShortImport)
        #self.df_short_acquire.clicked.connect(self.dfOpenAcquire)
        self.pdf_open_import.clicked.connect(self.pdfOpenImport)
        #self.pdf_open_acquire.clicked.connect(self.pdfOpenAcquire)
        self.pdf_short_import.clicked.connect(self.pdfShortImport)
        #self.pdf_short_acquire.clicked.connect(self.pdfShortAcquire)
        self.pdf_load_import.clicked.connect(self.pdfLoadImport)
        #self.pdf_load_acquire.clicked.connect(self.pdfLoadAcquire)

        self.addPlug.clicked.connect(self.addNewPlug)
        self.addPlug.setEnabled(False)

        self.dialog.exec_()

    def dfOpenImport(self):
        self.dfOpen = self.importSNP()
        self.df_open_label.setText(self.dfOpen.split('/')[-1])
        self.createPlug()

    def dfShortImport(self):
        self.dfShort = self.importSNP()
        self.df_short_label.setText(self.dfShort.split('/')[-1])
        self.createPlug()

    def pdfOpenImport(self):
        self.pdfOpen = self.importSNP()
        self.pdf_open_label.setText(self.pdfOpen.split('/')[-1])
        self.createPlug()

    def pdfShortImport(self):
        self.pdfShort = self.importSNP()
        self.pdf_short_label.setText(self.pdfShort.split('/')[-1])
        self.createPlug()

    def pdfLoadImport(self):
        self.pdfLoad = self.importSNP()
        self.pdf_load_label.setText(self.pdfLoad.split('/')[-1])
        self.createPlug()

        

    def createPlug(self, plugName = None):

        condition = self.dfOpen and self.dfShort and self.pdfOpen and self.pdfShort and self.pdfLoad

        if condition:  #if all the required measurements are there
            correctedPlugVector = self.em.addPlug(self.dfOpen , self.dfShort , self.pdfOpen , self.pdfShort , self.pdfLoad, plugName)

            self.addPlug.setEnabled(True)

            if plugName == None:

                self.correctedPlugVectorPhase = {}


                
                for pair in correctedPlugVector.keys():
                    self.correctedPlugVectorPhase[pair] = np.angle(correctedPlugVector[pair], deg = True)
                    

                self.plot()


    def importSNP(self):
        options = self.Options()
        options |= self.DontUseNativeDialog
        file, _ = self.getOpenFileName(self,"QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            print(file)
            return file


    def getPhaseLimits(self):
        tpLim = {}

        f100 = list(self.em.freq).index(100)
        f500 = list(self.em.freq).index(500)

        freq = np.array(self.em.freq[f100:f500]) / 1e6
        tpLim["45-36"] = {}
        tpLim["45-36"]["+"] = [(-90 + 1.5*f/100) + 1 if f in range(1, 500) else (-90 + 1.5*f/100) + f/100 for f in freq]
        tpLim["45-36"]["-"] = [(-90 + 1.5*f/100) - 1 if f in range(1, 500) else (-90 + 1.5*f/100) - f/100 for f in freq]
        
        tpLim["12-36"] = {}
        tpLim["12-36"]["+"] = [(-90 + 1.5*f/100) + 3*f/100 for f in freq]
        tpLim["12-36"]["-"] = [(-90 + 1.5*f/100) - 3*f/100 for f in freq]

        tpLim["36-78"] = {}
        tpLim["36-78"]["+"] = [(-90 + 1.5*f/100) + 3*f/100 for f in freq]
        tpLim["36-78"]["-"] = [(-90 + 1.5*f/100) - 3*f/100 for f in freq]


        tpLim["45-12"] = {}
        tpLim["45-12"]["+"] = [90 + (30*f/100) for f in freq]
        tpLim["45-12"]["-"] = [90 - (30*f/100) for f in freq]

        tpLim["45-78"] = {}
        tpLim["45-78"]["+"] = [90 + (30*f/100) for f in freq]
        tpLim["45-78"]["-"] = [90 - (30*f/100) for f in freq]

        tpLim["12-78"] = None
        
        return tpLim
        
    def plot(self):

        limit = self.getPhaseLimits()
        
        self.graphicsView.figure.clear()
        for i, pair in enumerate(self.correctedPlugVectorPhase):
            f100 = list(self.em.freq.astype(int)).index(100)
            f500 = list(self.em.freq.astype(int)).index(500)

            ax=self.graphicsView.figure.add_subplot(3, 2, i+1)
            ax.semilogx(self.em.freq[f100: f500], self.correctedPlugVectorPhase[pair][f100: f500])

            ax.set_ylim((-100, 300))

            if limit[pair]:
                ax.semilogx(self.em.freq[f100: f500], limit[pair]["+"])
                ax.semilogx(self.em.freq[f100: f500], limit[pair]["-"])

                ax.set_ylim((min(limit[pair]["-"]) - 5), max(limit[pair]["+"])+5)
    
            ax.grid(which="both")

            ax.set_title(pair)

            ax.set_xlabel('Freq (Hz)')
            ax.set_ylabel('dB')

        self.graphicsView.draw()

    def addNewPlug(self):

        plugName = self.plug_name_line_edit.text()
        try:

            self.createPlug(plugName)
            self.dialog.close()
        except Exception as e:
            print("file already exists")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)

            msg.setText("A plug by this name already exists.")
            msg.setInformativeText("Please rename your plug")
            msg.setWindowTitle("Plug name conflict")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
               
            retval = msg.exec_()  

def main():
    app = QtWidgets.Dialog()  # A new instance of QApplication
    app.setStyle('fusion')
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()


    form = AddPlug()  # We set the  form to be our ExampleApp (design)

    #form.show()  # Show the form
    form.show()

    sys._excepthook = sys.excepthook
    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = exception_hook
    #splash.finish(form)

    sys.exit(app.exec_())

if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
