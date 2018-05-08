from Sample import Sample
from alien import Alien

from embedding2 import Embedding

import threading
from PyQt5 import QtWidgets, QtGui
import time

import xlsxwriter
import os
import subprocess


class Project: #Put (object) later

    def __init__(self):
 
        self.measurements = [] #array of sample objects
        self.activeMeasurements = []
    
    def importSNP(self, samples):

        if len(samples) == 0:
            return -1
            
        start_time = time.time()

        threads = []
        num_meas = len(self.measurements)
    
 
        for idx, sample in enumerate(samples):
            self.measurements.append(Sample(sample))
            #self.measurements[idx].getParameters()
            
            t = threading.Thread(target=self.measurements[num_meas+idx].getParameters())
            threads.append(t)
            t.start()
            print("starting")
            
        for t in threads:
            print("done")
            t.join()

        #print self.measurements
        #print("--- %s seconds ---" % (time.time() - start_time))        

        #TODO: Add selected samples

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

    def generateExcel(self, outputName, samples):
        workbook = xlsxwriter.Workbook(outputName)
        for sample in samples:
            print(sample)
            sample = self.getSampleByName(sample)
            print(sample)
            worksheet = workbook.add_worksheet(sample.name)
            worksheet.write('A1', 'Sample ID:')
            worksheet.write('B1', sample.name)

            cell_format = workbook.add_format({'align': 'center',
                                               'valign': 'vcenter'})
            worksheet.merge_range('A4:A5', "", cell_format)
            worksheet.write('A4', "Frequency")
            for i, f in enumerate(sample.freq):
                worksheet.write(5+i,0, f)

            curPos = 1
            for i, param in enumerate(sample.parameters):
                numSignals = len(getattr(sample, param.replace(" ", "")).keys())
                worksheet.merge_range(3, curPos, 3, curPos+numSignals-1,  "", cell_format)
                worksheet.write(3,curPos, param)
                keys = sorted(getattr(sample, param.replace(" ", "")).keys())
                for i, key in enumerate(keys):
                    worksheet.write(4,curPos+i, key)
            
                    for j,data in enumerate(getattr(sample, param.replace(" ", ""))[key]):
                        worksheet.write(5+j,curPos+i, str(data))
        
                curPos += numSignals
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
    proj1.generateExcel("test1.xlsx", ["TestPCLiam3","TestPCLiam4"])


    
    
    
