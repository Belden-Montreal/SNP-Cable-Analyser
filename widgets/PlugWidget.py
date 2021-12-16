from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox

import sys
import scipy

from UI import plugDialog
from UI import VNA_addr_dialog
from UI import TestParameters

from UI import plugWidget as PW


from Communication import Communication
from embedding import Embedding
from plug import Plug


import matplotlib.figure
import matplotlib.backends.backend_qt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.pyplot import cm

import numpy as np


class PlugWidget():

    def __init__(self, parentTab, graph, sample, comm=None):
        super(self.__class__, self).__init__()

        self.widget  = QtWidgets.QWidget()
        self.plugWidget = PW.Ui_PlugWidget()
        self.plugWidget.setupUi(self.widget)

        self.parentTab = parentTab
        self.sample = sample
        self.graphicsView = graph

        self.plugTab = QtWidgets.QWidget()
        #self.TPNextPhaseTab = QtWidgets.QWidget()
        self.plugWidget = PW.Ui_PlugWidget()
        self.plugWidget.setupUi(self.plugTab)



        self.plug = sample

        self.dfOpen = self.plug.dfOpen
        self.dfShort = self.plug.dfShort
        self.pdfOpen = self.plug.pdfOpen
        self.pdfShort = self.plug.pdfShort
        self.pdfLoad = self.plug.pdfLoad
        self.correctedPlugVectorPhase = {}  

        font = QtGui.QFont()
        font.setPointSize(7)

        self.plugWidget.df_open_label.setFont(font)
        self.plugWidget.df_short_label.setFont(font)
        self.plugWidget.pdf_open_label.setFont(font)
        self.plugWidget.pdf_short_label.setFont(font)
        self.plugWidget.pdf_load_label.setFont(font)
        '''Here we will connect the buttons (import/acquire) to their apropriate functions'''

        self.plugWidget.df_open_import.clicked.connect(self.dfOpenImport)
        #self.df_open_acquire.clicked.connect(self.dfOpenAcquire)
        self.plugWidget.df_short_import.clicked.connect(self.dfShortImport)
        #self.df_short_acquire.clicked.connect(self.dfOpenAcquire)
        self.plugWidget.pdf_open_import.clicked.connect(self.pdfOpenImport)
        #self.pdf_open_acquire.clicked.connect(self.pdfOpenAcquire)
        self.plugWidget.pdf_short_import.clicked.connect(self.pdfShortImport)
        #self.pdf_short_acquire.clicked.connect(self.pdfShortAcquire)
        self.plugWidget.pdf_load_import.clicked.connect(self.pdfLoadImport)
        #self.pdf_load_acquire.clicked.connect(self.pdfLoadAcquire)
        
        #self.cancelButton.clicked.connect(self.cancel)

        self.plugWidget.calculate.clicked.connect(self.createPlug)
        self.plugWidget.calculate.setEnabled(True)    #CHANGE TO FALSE ! (True only for testing)

        self.plugWidget.save_plug.clicked.connect(self.savePlug)

        '''For testing (comment out later)'''
        self.dfOpen = "snps/DEEMBED TEST/DirectFixOpen.s8p"
        self.dfShort = "snps/DEEMBED TEST/DirectFixShort.s8p"
        self.pdfOpen = "snps/DEEMBED TEST/DirectFixPlugOpen.s8p"
        self.pdfShort = "snps/DEEMBED TEST/DirectFixPlugShort.s8p"
        self.pdfLoad = "snps/DEEMBED TEST/DirectFixPlugLoad2.s8p"
        

        ''' End of "for testing"'''

        #self.plugWidget.setupUi(self.plugTab)
        self.plugUpdateTab()
        self.updateDelayLabels()

    def dfOpenImport(self):
        try:
            self.dfOpen = self.importSNP()
            self.plugWidget.df_open_label.setText(self.dfOpen.split('/')[-1])
            self.enableCalcButton()
        
        except Exception as e:
            print(e)

    def dfShortImport(self):
        try:
            self.dfShort = self.importSNP()
            self.plugWidget.df_short_label.setText(self.dfShort.split('/')[-1])
            self.enableCalcButton()
       
        except Exception:
            return

    def pdfOpenImport(self):
        try:
            self.pdfOpen = self.importSNP()
            self.plugWidget.pdf_open_label.setText(self.pdfOpen.split('/')[-1])
            self.enableCalcButton()
        except Exception:
            return

    def pdfShortImport(self):
        try:
            self.pdfShort = self.importSNP()
            self.plugWidget.pdf_short_label.setText(self.pdfShort.split('/')[-1])
            self.enableCalcButton()

        except Exception:
            return

    def pdfLoadImport(self):
        try:
            self.pdfLoad = self.importSNP()
            self.plugWidget.pdf_load_label.setText(self.pdfLoad.split('/')[-1])
            self.enableCalcButton()
        except Exception:
            return

    def enableCalcButton(self):
        self.plug.calculated = False
        condition = self.dfOpen and self.dfShort and self.pdfOpen and self.pdfShort and self.pdfLoad
        if condition:
            self.plugWidget.calculate.setEnabled(True)
        else:
            self.plugWidget.calculate.setEnabled(False)




    def createPlug(self, plugName = None):


        correctedPlugVector = self.plug.addPlug(self.dfOpen , self.dfShort , self.pdfOpen , self.pdfShort , self.pdfLoad, plugName)

        #self.addPlug.setEnabled(True)

        '''if plugName == None:

            self.correctedPlugVectorPhase = {}'''

        #print("Corrected Plug Vect Phase : ", self.correctedPlugVectorPhase)
        #self.plot()

        self.limit = self.getPhaseLimits()

        self.plugUpdateTab()

        self.plugWidget.save_plug.setEnabled(True)   
        self.updateDelayLabels()

    def updateDelayLabels(self):
        if self.plug.calculated:
            self.plugWidget.dnext12_36.setText(str(self.plug.plugNextDelay["12-36"]))
            self.plugWidget.dnext45_12.setText(str(self.plug.plugNextDelay["45-12"]))
            self.plugWidget.dnext12_78.setText(str(self.plug.plugNextDelay["12-78"]))
            self.plugWidget.dnext45_36.setText(str(self.plug.plugNextDelay["45-36"]))
            self.plugWidget.dnext36_78.setText(str(self.plug.plugNextDelay["36-78"]))
            self.plugWidget.dnext45_78.setText(str(self.plug.plugNextDelay["45-78"]))


    def importSNP(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileNames()", "","sNp Files (*.s*p)", options=options)
        #print files
        if file:
            print(file)
            return file


    def getPhaseLimits(self):
        tpLim = {}

        f100 = list(self.plug.freq.astype(int)).index(100)
        f500 = list(self.plug.freq.astype(int)).index(500)

        freq = np.array(self.plug.freq[f100:f500]) / 1e6
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

    def plugPlotUpdate(self, activeParameter):
        self.activeParameter = activeParameter
        sample = self.sample
        limit = None
        H_limit_mag=None
        H_limit_phase = None
        L_limit_mag = None
        L_limit_phase = None
        if sample.standard is not None:
            if "TPMag " + self.activeParameter + " H" in sample.standard.limits:
                H_limit_mag = sample.standard.limits["TPMag " + self.activeParameter + " H"].getArray()
                print("yes ! ")
            if "TPP " + self.activeParameter + " H" in sample.standard.limits:
                H_limit_phase = sample.standard.limits["TPP " + self.activeParameter + " H"].getArray()            
            if "TPMag " + self.activeParameter + " L" in sample.standard.limits:
                L_limit_mag = sample.standard.limits["TPMag " + self.activeParameter + " L"].getArray()
                print("yes ! ")

            if "TPP " + self.activeParameter + " L" in sample.standard.limits:
                L_limit_phase = sample.standard.limits["TPP " + self.activeParameter + " L"].getArray()       
        

        self.plot(activeParameter, h_lim_mag = H_limit_mag, h_lim_ph = H_limit_phase, l_lim_mag = L_limit_mag, l_lim_ph=L_limit_phase)

    def plot(self, activeParameter, h_lim_mag=None, h_lim_ph=None, l_lim_mag=None, l_lim_ph=None):


        if activeParameter != "Plug Main":
            self.graphicsView.figure.clear()

            if activeParameter not in self.plug.correctedPlugVectorPhase.keys():
                print(self.plug.correctedPlugVectorPhase.keys())
                print(activeParameter, "not here")
                return



        self.graphicsView.figure.clear()
        f100 = list(self.plug.freq.astype(int)).index(100)
        f500 = list(self.plug.freq.astype(int)).index(500)

        ax=self.graphicsView.figure.add_subplot(1, 2, 1)
        ax.grid(which="both")

        ax.set_title("Test Plug Mag. " + activeParameter)

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('dB')
        ax.semilogx(self.plug.freq, self.plug.correctedPlugVectorMag[activeParameter], label=activeParameter)
        if h_lim_mag:
            ax.semilogx(*zip(*h_lim_mag), label = "Upper Limit")
        if l_lim_mag:
            print("Plot got l lmim mag")
            ax.semilogx(*zip(*l_lim_mag), label = "Lower Limit")
        #ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())


        ax=self.graphicsView.figure.add_subplot(1, 2, 2)
        ax.grid(which="both")
        ax.set_title("Test Plug Phase " + activeParameter)

        ax.set_xlabel('Freq (MHz)')
        ax.set_ylabel('deg')

        ax.semilogx(self.plug.freq, self.plug.correctedPlugVectorPhase[activeParameter])
        if h_lim_ph:
            ax.semilogx(*zip(* h_lim_ph), label = "Upper Limit")
        if l_lim_ph:
            ax.semilogx(*zip(*l_lim_ph), label = "Lower Limit")
        ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

        self.graphicsView.figure.tight_layout(pad=3.0)
        self.graphicsView.draw()


    def plugUpdateTab(self):
        try:
            self.plugWidget.df_open_label.setText(self.dfOpen.split('/')[-1])
            self.plugWidget.df_short_label.setText(self.dfShort.split('/')[-1])
            self.plugWidget.pdf_open_label.setText(self.pdfOpen.split('/')[-1])
            self.plugWidget.pdf_short_label.setText(self.pdfShort.split('/')[-1])
            self.plugWidget.pdf_load_label.setText(self.pdfLoad.split('/')[-1])

        except:
            pass
        
        self.parentTab.clear()

        self.parentTab.addTab(self.plugTab, "Plug Main")        

        if self.plug.correctedPlugVectorPhase:

            #self.embeded_tab_list = []

            for key in self.plug.correctedPlugVectorPhase.keys():
                self.new_plugtab = QtWidgets.QWidget()
                #self.embeded_tab_list.append(self.new_plugtab)
                self.parentTab.addTab(self.new_plugtab, key)
                

    def savePlug(self, file):
        outputFile, _ = QFileDialog.getSaveFileName(None, "Save Plug", "","Plug file (*.plug)")
        self.plug.serialize(file = outputFile)


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
