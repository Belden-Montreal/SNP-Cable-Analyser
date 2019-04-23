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
        worksheet.write('A1', 'Plug ID:')
        worksheet.write('B1', sample.getName())
    
        cell_format = workbook.add_format({'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 6,})
        worksheet.merge_range('A3:A5', "Frequency", cell_format)

        curPos = 1
        parameters = {"RL": sample.getParameters()["RL"], "CNEXT": sample.getParameters()["CNEXT"]}
        for i, (paramName, parameter) in enumerate(parameters.items()):
            numSignals = len(parameter.getPorts())
            worksheet.merge_range(2, curPos, 2, curPos+numSignals*2-1,  paramName, cell_format)
            for i, (key, (portName,_)) in enumerate(parameter.getPorts().items()):
                worksheet.merge_range(3, curPos+i*2, 3, curPos+i*2+1, str(portName), cell_format)
                if paramName == "Propagation Delay":
                    worksheet.merge_range(4, curPos+i*2, 4, curPos+i*2+1, "ns", cell_format)
                    param = parameter.getParameter()
                    for j, data in enumerate(param[key]):
                        worksheet.merge_range(5+j, curPos+i*2, 5+j, curPos+i*2+1, "")
                        self.box(workbook, worksheet, param, key, i*2, j, data, curPos)
                else:
                    worksheet.write(4,curPos+i*2, "mag", cell_format)
                    worksheet.write(4,curPos+i*2+1, "phase", cell_format)
                    param = parameter.getParameter()
                    for j, (mag, phase) in enumerate(param[key]):
                        worksheet.write(5+j, 0, sample.getFrequencies()[j])
                        self.box(workbook, worksheet, param, key, i*2, j, mag, curPos)
                        self.box(workbook, worksheet, param, key, i*2+1, j, phase, curPos)
        
            curPos += numSignals*2
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
