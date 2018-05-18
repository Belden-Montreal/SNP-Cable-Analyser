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


class addPlug(QtWidgets.QMainWindow, plugDialog.Ui_Dialog, QtWidgets.QAction, QtWidgets.QFileDialog, QtWidgets.QListView, QtWidgets.QDialog, QtCore.Qt):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

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

        if condition:
            correctedPlugVector = self.em.addPlug(self.dfOpen , self.dfShort , self.pdfOpen , self.pdfShort , self.pdfLoad, plugName)
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

    def plot(self):

        self.graphicsView.figure.clear()

        x = np.array([i for i in range(0, 500)])

        ax=self.graphicsView.figure.add_subplot(321)
        #a = scipy.signal.decimate(x, 10)
        ax.plot(self.em.freq, self.correctedPlugVectorPhase['45-12'])


        ax.grid(which="both")

        ax.set_xlabel('Freq (Hz)')
        ax.set_ylabel('dB')

        ax=self.graphicsView.figure.add_subplot(322)
        ax.semilogx(x, x**2)


        ax.grid(which="both")

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('dB')

        
        ax=self.graphicsView.figure.add_subplot(323)
        ax.semilogx(x, x**2)


        ax.grid(which="both")

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('dB') 


        ax=self.graphicsView.figure.add_subplot(324)
        ax.semilogx(x, x**2)


        ax.grid(which="both")

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('dB')


        ax=self.graphicsView.figure.add_subplot(325)
        ax.semilogx(x, x**2)


        ax.grid(which="both")

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('dB')



        ax=self.graphicsView.figure.add_subplot(326)
        ax.semilogx(x, x**2)


        ax.grid(which="both")

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('dB') 
        self.graphicsView.draw()




        

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    app.setStyle('fusion')
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()


    form = addPlug()  # We set the  form to be our ExampleApp (design)

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
