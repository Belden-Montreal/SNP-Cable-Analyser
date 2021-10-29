from Sample import Sample
from alien import Alien
from embedding import Embedding

import threading
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import time

import xlsxwriter
import os
import subprocess


from pathos.pools import ProcessPool
from multiprocessing import cpu_count

class Project(): #Put (object) later

    def __init__(self):
         
        super(self.__class__, self).__init__()

        self.measurements = [] #array of sample objects
        self.activeMeasurements = []
        
        self.threadPool = []

    def importSNP(self, files):
        
        start_time = time.time()
        threads = []
        num_meas = len(self.measurements)
        #for idx, sample in enumerate(samples):

        with ProcessPool(cpu_count()) as p:
            samples = p.map(self.addSample, files)
        
            for s in samples:
                self.measurements.append(s)

        return

        '''my_thread = QtCore.QThread(self)
            my_thread.start()
            my_thread.wait()
            my_worker = GenericWorker(self.startSNPImport, snpFile = sample)
            my_worker.moveToThread(my_thread)
            my_worker.finished.connect(self.finishSNPImport)

            #self.my_worker.start.connect(self.my_worker)
            my_worker.start.emit()
            self.threadPool.append(my_thread)
        for t in self.threadPool:
            if not t.isRunning():
                # get results from thread
                t.handled = True
        my_threads = [t for t in my_threads if not t.handled]
        '''





        #print self.measurements
        #print("--- %s seconds ---" % (time.time() - start_time))        
        #TODO: Add selected samples

    def addSample(self, file):
        s = Sample(file)
        s.getParameters()
        return s
        
    def delete(self, samples):
        for sample in samples:
            sample = self.getSampleByName(sample)

            print("Sample Name:" , sample)
            for idx, measurement in enumerate(self.measurements):
                if measurement is sample:
                    print(idx)
                    del self.measurements[idx]

            #print("Sample Index:", sample.ref )
            

    def addEmbed(self, testName):
        self.measurements.append(Embedding(testName))
        
    def addAlien(self, testName):              
 
        self.measurements.append(Alien(testName))

    def setStandard(self, *args):
        pass

    def assignPorts(self, *args):
        pass

    def generatePdf(self, *args):
        pass

    def addLimit(self):
        pass

    def getSampleByName(self, name):
        return next((sample for sample in self.measurements if sample.name==name),None)

    def generateExcel(self, outputName, samples, z = False):
        workbook = xlsxwriter.Workbook(outputName)
        for sample in samples:
            print(sample)
            sample = self.getSampleByName(sample)
            print(sample)
            worksheet = workbook.add_worksheet(sample.name)
            worksheet.write('A1', 'Sample ID:')
            worksheet.write('B1', sample.name)


            if(sample.__retr__() == "SNP"):

                cell_format = workbook.add_format({'align': 'center',
                                                   'valign': 'vcenter'})
                worksheet.merge_range('A4:A5', "", cell_format)
                worksheet.write('A4', "Frequency")
                for i, f in enumerate(sample.freq):
                    worksheet.write(5+i,0, f)

                curPos = 1
                for i, param in enumerate(sample.parameters):
                    numSignals = len(getattr(sample, param.replace(" ", "")).keys())
                    if z is False:
                        worksheet.merge_range(3, curPos, 3, curPos+numSignals-1,  "", cell_format)
                        worksheet.write(3,curPos, param)
                        keys = sorted(getattr(sample, param.replace(" ", "")).keys())
                        for i, key in enumerate(keys):
                            worksheet.write(4,curPos+i, key)
                    
                            for j,data in enumerate(getattr(sample, param.replace(" ", ""))[key]):
                                worksheet.write(5+j,curPos+i, data)
                
                        curPos += numSignals
                    else:
                        worksheet.merge_range(2, curPos, 2, curPos+(numSignals-1)*2,  "", cell_format)
                        worksheet.write(2,curPos, param)
                        keys = sorted(getattr(sample, param.replace(" ", "")).keys())
                        for i, key in enumerate(keys):
                            worksheet.merge_range(3, curPos+i*2, 3, curPos+i*2+1, "", cell_format)
                            worksheet.write(3,curPos+i*2, key)
                            worksheet.write(4,curPos+i*2, "real")
                            worksheet.write(4,curPos+i*2+1, "imaginary")
                            for j,data in enumerate(getattr(sample, param.replace(" ", "")+"Z")[key]):
                                worksheet.write(5+j,curPos+i*2, data.real)
                                worksheet.write(5+j, curPos+i*2+1, data.imag)
                
                        curPos += numSignals*2
        workbook.close()
        
    @property
    def activeSample(self):
        return [sample.name for sample in self.activeMeasurements]
    
    @activeSample.setter
    def activeSample(self, samples):
        self.activeMeasurements = [self.getSampleByName(sample) for sample in samples]
        
if __name__ == '__main__':  
    proj1 = Project()

    proj1.importSNP([r"snps\TestPCLiam3.s8p", r"snps\TestPCLiam4.s8p"])

    print(proj1.getSampleByName(u"TestPCLiam3"))
    #proj1.generateExcel("test1.xlsx", ["TestPCLiam3","TestPCLiam4"])


    
    
    
