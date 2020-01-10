from snpanalyzer.project.project import Project, ProjectNode
from snpanalyzer.parameters.type import ParameterType
from snpanalyzer.sample.delay import DelaySample
from snpanalyzer.sample.plugdelay import PlugDelaySample
from snpanalyzer.gui.dialog.plug_import_dialog import PlugImportDialog
import numpy as np
import xlsxwriter

class Plug(Project):

    def __init__(self, name):
        super(Plug, self).__init__(name)
        self._openDelay = None
        self._shortDelay = None
        self._loadSample = None
        self._dfOpenDelay = None
        self._dfShortDelay = None
        self._k1 = 0
        self._k2 = 0
        self._k3 = 0
        self.type = "Plug"
        self._ports=None

    def getSamples(self):
        return [self._openDelay,self._shortDelay,self._dfOpenDelay,self._dfShortDelay]

    def getType(self):
        return self.type

    def getOpenDelay(self):
        return self._openDelay

    def getShortDelay(self):
        return self._shortDelay

    def getLoadSample(self):
        return self._loadSample

    def getDfOpenDelay(self):
        return self._dfOpenDelay

    def getDfShortDelay(self):
        return self._dfShortDelay

    def importDfOpen(self, fileName):
        self._dfOpenDelay = DelaySample(fileName)
        return self._dfOpenDelay

    def importDfShort(self, fileName):
        self._dfShortDelay = DelaySample(fileName)
        return self._dfShortDelay

    def importOpen(self, fileName):
        self._openDelay = DelaySample(fileName)
        return self._openDelay

    def importShort(self, fileName):
        self._shortDelay = DelaySample(fileName)
        return self._shortDelay

    def importLoad(self, fileName):
        self._loadSample = PlugDelaySample(fileName, 
            self._openDelay.getParameter(ParameterType.PROPAGATION_DELAY),
            self._shortDelay.getParameter(ParameterType.PROPAGATION_DELAY),
            self._dfOpenDelay.getParameter(ParameterType.PROPAGATION_DELAY),
            self._dfShortDelay.getParameter(ParameterType.PROPAGATION_DELAY),
            self._k1, self._k2, self._k3)
        return self._loadSample

    def getPlugNext(self):
        if self._loadSample:
            return self._loadSample.getParameter(ParameterType.CORRECTED_NEXT)
        return None

    def getNextDelay(self):
        return self._loadSample.getParameters()[ParameterType.NEXT_DELAY]

    def getPlugDelay(self):
        return self._loadSample.getParameters()[ParameterType.PLUG_DELAY]

    def setConstants(self, k1, k2, k3):
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3

    def recalculate(self):
        self._loadSample.recalculate(self._k1, self._k2, self._k3)

    def getConstants(self):
        return (self._k1, self._k2, self._k3)

    def nodeFromProject(self):
        return PlugNode(self)

    def removeSample(self, sample):
        if self._dfOpenDelay == sample:
            self._dfOpenDelay = None
        if self._dfShortDelay == sample:
            self._dfShortDelay = None
        if self._openDelay == sample:
            self._openDelay = None
        if self._shortDelay == sample:
            self._shortDelay = None
        if self._loadSample == sample:
            self._loadSample = None

    def dfOpen(self):
        return self._dfOpenDelay

    def dfShort(self):
        return self._dfShortDelay

    def openSample(self):
        return self._openDelay

    def shortSample(self):
        if self._shortDelay is not None:
            print("Short Sample name is : ", self._shortDelay.getFileName())
        return self._shortDelay

    def loadSample(self):
        return self._loadSample

    def generateExcel(self, outputName, sampleNames, z=False):
        workbook = xlsxwriter.Workbook(outputName, options={'nan_inf_to_errors': True})
        sample = self._loadSample
        worksheet = workbook.add_worksheet(sample.getName())

        cell_format = workbook.add_format({'align': 'center',
                                           'valign': 'vcenter',
                                           'border': 6, })
        worksheet.merge_range('A3:A5', "Frequency", cell_format)
        worksheet.write('A1', 'Plug ID:')
        worksheet.write('B1', sample.getName())
        curPos=1

        for parameter in [sample.getParameter(ParameterType.CORRECTED_NEXT),sample.getParameter(ParameterType.RL)]:
            try:
                numSignals = len(parameter.getParameter().keys())
            except:
                continue
            paramName = parameter.getName()
            worksheet.merge_range(2, curPos, 2, curPos + numSignals * 2 - 1, paramName, cell_format)
            for i, portName in enumerate(sorted(list(parameter.getDataSeries()), key=lambda
                    params: params.getName())):  # enumerate(list(parameter.getDataSeries())):
                portSeries = portName
                # print(parameter)
                portName = portName.getName()
                worksheet.merge_range(3, curPos + i * 2, 3, curPos + i * 2 + 1, str(portName), cell_format)
                if z:
                    worksheet.write(4, curPos + i * 2, "real", cell_format)
                    worksheet.write(4, curPos + i * 2 + 1, "imaginary", cell_format)
                    param = parameter.getComplexParameter()
                    for j, data in enumerate(param[portSeries]):
                        worksheet.write(5 + j, 0, sample.getFrequencies()[j])
                        self.box(workbook, worksheet, param, portSeries, i * 2, j, data.real, curPos)
                        self.box(workbook, worksheet, param, portSeries, i * 2 + 1, j, data.imag, curPos)

                else:
                    worksheet.write(4, curPos + i * 2, "mag", cell_format)
                    worksheet.write(4, curPos + i * 2 + 1, "phase", cell_format)
                    param = parameter.getParameter()

                        # print(param[portSeries])
                    try:
                        if type(param[portSeries]) is not list:
                            param[portSeries] = [param[portSeries]]
                        for j, (mag, phase) in enumerate(list(param[portSeries])):
                                worksheet.write_number(5 + j, 0, sample.getFrequencies()[j])
                                self.box(workbook, worksheet, param, portSeries, i * 2, j, mag, curPos)
                                self.box(workbook, worksheet, param, portSeries, i * 2 + 1, j, phase, curPos)
                    except Exception as e:
                        print(e)

            curPos += numSignals*2
        '''worksheet = workbook.add_worksheet(sample.getName())
        worksheet.write('A1', 'Plug ID:')
        worksheet.write('B1', sample.getName())
    
        cell_format = workbook.add_format({'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 6,})
        
        
        
        
        
        #This first page will contain a summery of the plug 

        worksheet.merge_range("B3:D3", "Constants", cell_format)
        worksheet.write("B4", "SJ 12, 45, 78", cell_format)
        worksheet.write("C4", "SJ 36", cell_format)
        worksheet.write("D4", "Thru Calib", cell_format)
        worksheet.write("B5", self._k1, cell_format)
        worksheet.write("C5", self._k2, cell_format)
        worksheet.write("D5", self._k3, cell_format)

        print("Next Delay ",self.getNextDelay().getDataSeries())

        #Exporting Next Delay
        series = self.getNextDelay().getDataSeries()
        print("series ", len(series))
        next_delay = self.getNextDelay().getParameter()
        worksheet.merge_range(2,5,2,5+len(series)-1, "Next Delay (DNEXT)", cell_format)
        for i, portSeries in enumerate(sorted(list(series), key=lambda params: params.getName())):#enumerate(list(parameter.getDataSeries())):
            if type(next_delay) is not list:
                next_delay[portSeries] = [next_delay[portSeries]] 
            for j, (mag) in enumerate(list(next_delay[portSeries])):
                #worksheet.write(5+j, 0, sample.getFrequencies()[j])
                worksheet.write(3, 5+i, portSeries.getName(), cell_format) 
                worksheet.write(4, 5+i, mag, cell_format) 

        #Exporting plug Delay
        series = self.getPlugDelay().getDataSeries()
        print("series ", len(series))
        plug_delay = self.getPlugDelay().getParameter()
        worksheet.merge_range(7,1,7,1+len(series)-1, "Plug Delay", cell_format)
        for i, portSeries in enumerate(sorted(list(series), key=lambda params: params.getName())):#enumerate(list(parameter.getDataSeries())):
            if type(plug_delay) is not list:
                plug_delay[portSeries] = [plug_delay[portSeries]] 
            for j, (mag) in enumerate(list(plug_delay[portSeries])):
                #worksheet.write(5+j, 0, sample.getFrequencies()[j])
                worksheet.write(8, 1+i, portSeries.getName(), cell_format) 
                worksheet.write(9, 1+i, mag, cell_format) 

        #worksheet.wirte()
                '''
        #building the second page with the Delays
        worksheet = workbook.add_worksheet("Delays")
        worksheet.merge_range('A3:A5', "Frequency", cell_format)
        curPos = 1
        for i, (paramName, parameter) in enumerate(sample.getParameters().items()):
            try:
                numSignals = len(parameter.getParameter().keys())
            except:
                continue
            paramName = str(paramName).replace("ParameterType.", "").replace("_", " ").split(":")[0]
            if "DELAY" in paramName:
                worksheet.merge_range(2, curPos, 2, curPos+numSignals-1,  paramName, cell_format)
                for i, portName in enumerate(sorted(list(parameter.getDataSeries()), key=lambda params: params.getName())):#enumerate(list(parameter.getDataSeries())):
                    portSeries = portName
                    #print(parameter)
                    portName = portName.getName()
                    worksheet.write(3, curPos + i, str(portName), cell_format)
                    worksheet.write(4, curPos + i , "ns", cell_format)
                    param = parameter.getParameter()
                    try:
                        if type(param[portSeries] ) is not list:
                                param[portSeries] = [param[portSeries]]
                        for j, mag in enumerate(list(param[portSeries])):
                                worksheet.write(5 + j, 0, sample.getFrequencies()[j])
                                self.box(workbook, worksheet, param, portSeries, i, j, mag, curPos, n=1)

                    except Exception as e:
                        print(e)
                curPos += numSignals

        #Writing the Constants
        worksheet.merge_range(2,curPos,2,curPos+2, "Constants", cell_format)
        worksheet.write(3,curPos, "SJ 12,45,78", cell_format)
        worksheet.write(3,curPos+1, "SJ 36", cell_format)
        worksheet.write(3,curPos+2, "Thru Calib", cell_format)
        worksheet.write(4,curPos, self._k1, cell_format)
        worksheet.write(4,curPos+1, self._k2, cell_format)
        worksheet.write(4, curPos+2, self._k3, cell_format)
        workbook.close()


from snpanalyzer.sample.sample import SampleNode
from snpanalyzer.gui.widget.plug_widget import PlugWidget
from snpanalyzer.app.node import Node
class PlugNode(ProjectNode):
    def __init__(self, plug):
        super(PlugNode, self).__init__(plug)
        self._plugWidget = None

    def openImportWindow(self, parent):
        dial = PlugImportDialog(parent)
        files = dial.getFiles()
        if files:
            dfOpen, dfShort, plugOpen, plugShort, plugLoad, k1, k2, k3 = files
            self._dataObject.importOpen(plugOpen)
            self._dataObject.importShort(plugShort)
            self._dataObject.importDfOpen(dfOpen)
            self._dataObject.importDfShort(dfShort)
            self._dataObject.setConstants(k1, k2, k3)
            self._dataObject.importLoad(plugLoad)

            self.updateChildren()
            if self._plugWidget:
                self._plugWidget.createTabs()
                self._plugWidget.updateWidget()

    def addChildren(self, samples):
        for sample in samples:
            self.appendRow(SampleNode(sample, self._dataObject))

    def addChildren(self, samples):
        pass
    
    def updateChildren(self):
        node = self.hasChild("DFOpen")
        if not node:
            node = Node("DFOpen")
            self.appendRow(node)
        node.setRowCount(0)
        if self._dataObject.dfOpen():
            node.appendRow(SampleNode(self._dataObject.dfOpen(), self._dataObject))

        node = self.hasChild("DFShort")
        if not node:
            node = Node("DFShort")
            self.appendRow(node)
        node.setRowCount(0)
        if self._dataObject.dfShort():
            node.appendRow(SampleNode(self._dataObject.dfShort(), self._dataObject))

        node = self.hasChild("Open")
        if not node:
            node = Node("Open")
            self.appendRow(node)
        node.setRowCount(0)
        if self._dataObject.openSample():
            node.appendRow(SampleNode(self._dataObject.openSample(), self._dataObject))

        node = self.hasChild("Short")
        if not node:
            node = Node("Short")
            self.appendRow(node)
        node.setRowCount(0)
        if self._dataObject.shortSample():
            node.appendRow(SampleNode(self._dataObject.shortSample(), self._dataObject))

        node = self.hasChild("Load")
        if not node:
            node = Node("Load")
            self.appendRow(node)
        node.setRowCount(0)
        if self._dataObject.loadSample():
            node.appendRow(SampleNode(self._dataObject.loadSample(), self._dataObject))  


    def setupInitialData(self):
        self.updateChildren()

    def getWidgets(self, vnaManager):
        if not self._plugWidget:
            self._plugWidget = PlugWidget(self, vnaManager)
        return {"Plug": self._plugWidget}



