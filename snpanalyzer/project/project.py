from snpanalyzer.analysis.parameter import ParameterAnalysis
from snpanalyzer.sample.cable import CableSample
from snpanalyzer.sample.plug import PlugSample
#from multiprocessing.dummy import Pool as ThreadPool
import threading
from snpanalyzer.gui.ui import MW
from os.path import splitext
import xlsxwriter
from PyQt5 import QtWidgets, QtGui
from pathlib import Path
class Project(object):
    '''
    The project class represents a simple project containing a number of regular samples.
    '''

    def __init__(self, name):
        self._name = name
        self._date = ""
        self.samplesList = []
        self._samples = list()
        self._standard = None
        self.type = "Other"

    def importSamples(self, fileNames):
        threads = []
        self.samplesList = []
        for sample in fileNames:
            print(len(fileNames))
            print("Importing  ", sample)
            t = threading.Thread(target=self.__createSample(sample))
            threads.append(t)
            t.start()
            print("starting")
        for t in threads:
            print("done")
            t.join()   
        self._samples.extend(self.samplesList)
        return self.samplesList 

    def __createSample(self, name):
        print("Sample name : "+ name)
        extension = Path(name).suffix
        print("file name "+name )
        print("extension "+extension )
        if extension[2] == "8" or extension[2] == "4":
            print("append")
            self.samplesList.append(PlugSample(name, standard=self._standard))
            return
        self.samplesList.append(CableSample(name, standard=self._standard))

    def removeSample(self, sample):
        if sample in self._samples:
            self._samples.remove(sample)

    def generateExcel(self, outputName, sampleNames, z=False):

        print("Starting Excel")
        #print("self.samples", self._samples[0].getName(), sampleNames)
      #  self.setStandard()
    #    for x in self._samples:
     #       print(x.getName())
        workbook = xlsxwriter.Workbook(outputName, options={'nan_inf_to_errors': True})
        samples = [x for x in self._samples]
       # samples = [x for x in self._samples if x.getName() in sampleNames]
        #for j in samples:
    #        print(j.getName())
       # for x in self._samples:
        #    print(x.getName())
        print("samples",samples)
        for i,sample in enumerate(samples):
            try:
                worksheet = workbook.add_worksheet(sample.getName())
                print(sample.getName())
            except Exception as e:
                print(e)
                worksheet = workbook.add_worksheet(sample.getName()+str(i))
            #sample.setStandard(sample.getStandard())
            worksheet.write('A1', 'Sample ID:')
            worksheet.write('B1', sample.getName())

            worksheet.write('A2', 'Sample Standard:')
            worksheet.write('B2', sample.getStandard().__str__())

            cell_format = workbook.add_format({'align': 'center',
                                                'valign': 'vcenter',
                                                'border': 6,})
            worksheet.merge_range('A3:A5', "Frequency", cell_format)

            curPos = 1  
            print("Done Setup")
            for i, (paramName, parameter) in enumerate(sample.getParameters().items()):
                #print(paramName)

                numSignals = len(parameter.getParameter().keys())
                print(str(paramName))

                paramName = str(paramName).replace("ParameterType.", "").replace("_", " ")
                worksheet.merge_range(2, curPos, 2, curPos+numSignals*2-1, paramName, cell_format)
                #print(parameter.getDataSeries().pop().getName())
                #print(parameter.getPorts()._ports.getName())

                #paramLimit = parameter.
              #  if parameter.getLimit() is not None:
              #      limit = True
             #   else:
              #      limit = False


                for i, portName in enumerate(parameter.getDataSeries()):#, key=lambda params: params.getName()):#enumerate(list(parameter.getDataSeries())):


                    portSeries = portName
                    portName = portName.getName()
                    print(str(portName))
                    worksheet.merge_range(3, curPos+i*2, 3, curPos+i*2+1, str(portName), cell_format)
                    if paramName == "PROPAGATION DELAY":
                        worksheet.merge_range(4, curPos+i*2, 4, curPos+i*2+1, "ns", cell_format)
                        param = parameter.getParameter()
                        for j, data in enumerate(param[portSeries]):
                            worksheet.merge_range(5+j, curPos+i*2, 5+j, curPos+i*2+1, "")
                            self.box(workbook, worksheet, param, portSeries, i*2, j, float(data), curPos)

                    else:
                        if z:
                            worksheet.write(4, curPos+i*2, "real", cell_format)
                            worksheet.write(4,curPos+i*2+1, "imaginary", cell_format)
                            param = parameter.getComplexParameter()
                            for j,data in enumerate(param[portSeries]):
                                worksheet.write(5+j, 0, sample.getFrequencies()[j])
                                self.box(workbook, worksheet, param, portSeries, i*2, j, data.real, curPos)
                                self.box(workbook, worksheet, param, portSeries, i*2+1, j, data.imag, curPos)
                        else:
                            worksheet.write(4,curPos+i*2, "mag", cell_format)
                            worksheet.write(4,curPos+i*2+1, "phase", cell_format)
                            param = parameter.getParameter()
                            print(param.keys())
                            for j, (mag,phase) in enumerate(param[portSeries]):
                                worksheet.write_number(5+j, 0, sample.getFrequencies()[j])
                                self.box(workbook, worksheet, param, portSeries, i*2, j, mag, curPos)
                                self.box(workbook, worksheet, param, portSeries, i*2+1, j, phase, curPos)
            
                curPos += numSignals*2
        workbook.close()

    def box(self, workbook, worksheet, parameter, port, i, j, data, curPos, n=2):
        box_form = workbook.add_format()

        if j == 0:
            box_form.set_top(6)
        if i == 0:
            box_form.set_left(6)
        if j == len(parameter[port])-1:
            box_form.set_bottom(6)

        if i == len(parameter)*n-1:
            box_form.set_right(6)

        if type(data) is not str:
            worksheet.write_number(j+5, curPos+i, data, box_form)
        else:
            worksheet.write(j+5, curPos+i, str(data), box_form)

    def findSamplesByName(self, names):
        return [x for x in self._samples if x.getName() in names]

    def numSamples(self):
        return len(self._samples)

    def samples(self):
        return self._samples

    def getSamples(self):
        return self._samples

    def getName(self):
        return self._name

    def getDate(self):
        return self._date

    def getType(self):
        return self.type

    def nodeFromProject(self):
        return ProjectNode(self)

    def setStandard(self, standard):
        self._standard = standard
        for sample in self._samples:
            sample.setStandard(standard)

from snpanalyzer.app.node import Node
from snpanalyzer.sample.sample import SampleNode
class ProjectNode(Node):
    def __init__(self, project):
        super(ProjectNode, self).__init__(project.getName())
        self._dataObject = project
        self.setupInitialData()

    def addChildren(self, samples):
        for sample in samples:
            self.appendRow(SampleNode(sample, self._dataObject))

    def openImportWindow(self, parent):
        names,_ = QtWidgets.QFileDialog.getOpenFileNames(parent, caption="Select SNP(s)", directory="",filter="sNp Files (*.s*p)")
        if names:
            self.addChildren(self._dataObject.importSamples(names))
            
    def addSamples(self, name):
        if name:
            self.addChildren(self._dataObject.importSamples(name))
        
     
    def delete(self):
        if self.parent():
            self.parent().removeRow(self.row())
        else:
            self.model().removeRow(self.row())

    def removeRow(self, row):
        QtGui.QStandardItem.removeRow(self, row)

    def setupInitialData(self):
        self.addChildren(self._dataObject.samples())

    def setStandard(self, standard):
        self._dataObject.setStandard(standard)


    # def getWidgets(self, vnaManager):
    #     return list()
    
##
##if __name__ == "main":
##
##    p = Project()
##    p.importSamples("cable3.s16p")
##    p.generateExcel("123", "cable3", True)
##    

