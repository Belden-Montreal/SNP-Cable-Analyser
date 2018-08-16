from project.project import Project, ProjectNode
from project.embedding_import_dialog import EmbedImportDialog, ReverseState
from app.save_manager import SaveManager
from sample.delay import CableDelaySample
from sample.plug import PlugSample 
from sample.deembed import DeembedSample, ReverseDeembedSample
from parameters.type import ParameterType
import numpy as np
import xlsxwriter

class Case():
    CAT5E = {
            1:((0,2),(lambda f, cnext: (-35.8+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            2:((0,2),(None)),
            3:((0,2),(None)),
            4:((0,2),(lambda f, cnext: (-39.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            5:((1,2),(lambda f, cnext: (-42+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            6:((1,2),(lambda f, cnext: (-50+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            7:((2,3),(lambda f, cnext: (-42+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            8:((2,3),(lambda f, cnext: (-50+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            9:((0,1),(lambda f, cnext: (-50+20*np.log10(f/100), 90))),
            10:((0,1),(None)),
            11:((0,3),(lambda f, cnext: (-50+20*np.log10(f/100), 90))),
            12:((0,3),(None)),
            13:((1,3),(lambda f, cnext: (-60+20*np.log10(f/100), 90))),
            14:((1,3),(None)),
            }
    CAT6 = {
            1:((0,2),(lambda f, cnext: (-38.1+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            2:((0,2),(lambda f, cnext: (-38.6+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            3:((0,2),(lambda f, cnext: (-39+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            4:((0,2),(lambda f, cnext: (-39.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            5:((1,2),(lambda f, cnext: (-46.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            6:((1,2),(lambda f, cnext: (-49.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            7:((2,3),(lambda f, cnext: (-46.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            8:((2,3),(lambda f, cnext: (-49.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            9:((0,1),(lambda f, cnext: (-57+20*np.log10(f/100), 90))),
            10:((0,1),(lambda f, cnext: (-70+20*np.log10(f/100), -90))),
            11:((0,3),(lambda f, cnext: (-57+20*np.log10(f/100), 90))),
            12:((0,3),(lambda f, cnext: (-70+20*np.log10(f/100), -90))),
            13:((1,3),(lambda f, cnext: (-66+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            14:((1,3),(lambda f, cnext: (-66+20*np.log10(f/100), np.angle(cnext, deg=True)-180))),
            }

class Embedding(Project):
    '''
    This class represents a project for analyzing plug embedding
    '''
    def __init__(self, name):
        super(Embedding, self).__init__(name)
        self._plug = None
        self._load = dict()
        self._load["Forward"] = None
        self._load["Reverse"] = None
        self._open = None
        self._short = None

    def importPlug(self, plugFile):
        self._plug = SaveManager().loadProject(plugFile)
        return self._plug

    def importLoad(self, loadFile, side, cat="CAT5e"):
        if cat == "CAT5e":
            cases = Case.CAT5E
        else:
            cases = Case.CAT6
        if side == "Forward":
            self._load[side] = DeembedSample(loadFile, self._plug.getPlugNext(), self._plug.getNextDelay(), cases)
        else:
            k1, k2, k3 = self._plug.getConstants()
            self._load[side] = ReverseDeembedSample(loadFile, self._plug.getPlugNext(), self._plug.getPlugDelay(),
                                              self._open.getParameter(ParameterType.PROPAGATION_DELAY), self._short.getParameter(ParameterType.PROPAGATION_DELAY), k1, k2, k3, cases)
        return self._load[side]

    def importOpen(self, openFile):
        self._open = PlugSample(openFile)
        return self._open

    def importShort(self, shortFile):
        self._short = PlugSample(shortFile)
        return self._short
    
    def removeSample(self, sample):
        for side in self._load:
            if sample == self._load[side]:
                self._load[side] = None
        if sample == self._open:
            self._open = None
        if sample == self._short:
            self._short = None

    def load(self):
        return self._load

    def openSample(self):
        return self._open
    
    def shortSample(self):
        return self._short

    def plug(self):
        return self._plug

    def generateExcel(self, outputName, sampleNames, z=False):
        workbook = xlsxwriter.Workbook(outputName, options={'nan_inf_to_errors': True})
        if z:
            dataTitle = ["Real", "Imag"]
        else:
            dataTitle = ["Mag", "Phase"]
        for side, sample in self._load.items():
            if sample:
                worksheet = workbook.add_worksheet(side)
                worksheet.write('A1', 'De-embedding ID:')
                worksheet.write('B1', sample.getName())
            
                cell_format = workbook.add_format({'align': 'center',
                                                    'valign': 'vcenter',
                                                    'border': 6,})
                worksheet.merge_range('A3:A5', "Frequency", cell_format)

                curPos = 1
                parameters = {"RL": sample.getParameters()["RL"], "NEXT": sample.getParameters()["NEXT"], "DNEXT": sample.getParameters()["DNEXT"], "Case": sample.getParameters()["Case"]}
                for (paramName, parameter) in (parameters.items()):
                    numSignals = len(parameter.getPorts())
                    if paramName == "Case":
                        nc = 0
                        for p in parameter.getParameter().values():
                            nc += len(p)
                        worksheet.merge_range(2, curPos, 2, curPos+nc*2-1,  paramName, cell_format)
                    else:
                        worksheet.merge_range(2, curPos, 3, curPos+numSignals*2-1,  paramName, cell_format)
                    for i, (key, (portName,_)) in enumerate(parameter.getPorts().items()):
                        if paramName == "Case":
                            param = self.__getParam(parameter, z)
                            numCases = len(param[key])
                            worksheet.merge_range(4, curPos, 4, curPos+numCases*2-1, str(portName), cell_format)
                            for k, (n, case) in enumerate(param[key].items()):
                                worksheet.merge_range(3, curPos+k*2, 3, curPos+k*2+1, str(n), cell_format)
                                worksheet.write(5,curPos+k*2, dataTitle[0], cell_format)
                                worksheet.write(5,curPos+k*2+1, dataTitle[1], cell_format)
                                for j, (data) in enumerate(case):
                                    d1,d2 = self.__getData(data, z)
                                    worksheet.write(6+j, 0, sample.getFrequencies()[j])
                                    self.box(workbook, worksheet, case, k*2, j, d1, curPos, numCases*2)
                                    self.box(workbook, worksheet, case, k*2+1, j, d2, curPos, numCases*2)
                            curPos+=numCases*2
                            
                        else:
                            worksheet.merge_range(4, curPos+i*2, 4, curPos+i*2+1, str(portName), cell_format)
                            worksheet.write(5,curPos+i*2, dataTitle[0], cell_format)
                            worksheet.write(5,curPos+i*2+1, dataTitle[1], cell_format)
                            param = self.__getParam(parameter, z)
                            for j, (data) in enumerate(param[key]):
                                d1,d2 = self.__getData(data, z)
                                worksheet.write(6+j, 0, sample.getFrequencies()[j])
                                self.box(workbook, worksheet, param[key], i*2, j, d1, curPos, len(param)*2)
                                self.box(workbook, worksheet, param[key], i*2+1, j, d2, curPos, len(param)*2)
                
                    curPos += numSignals*2
            workbook.close()

    def box(self, workbook, worksheet, case, i, j, data, curPos, nCases):
        box_form = workbook.add_format()
        if j == 0:
            box_form.set_top(6)
        if i == 0:
            box_form.set_left(6)
        if j == len(case)-1:
            box_form.set_bottom(6)
        if i == nCases-1:
            box_form.set_right(6)
        worksheet.write(j+6, curPos+i, data, box_form)
        
    def __getParam(self, param, z=False):
        if z:
            return param.getComplexParameter()
        else:
            return param.getParameter()

    def __getData(self, data, z=False):
        if z:
            return data.real, data.imag
        else:
            return data[0], data[1]

    def nodeFromProject(self):
        return EmbeddingNode(self)

    def setStandard(self, standard):
        for side in self._load.values():
            if side:
                side.setStandard(standard)


from app.node import Node
from sample.sample import SampleNode
from project.plug import PlugNode
from widgets.embed_widget import EmbedWidget
from PyQt5 import QtWidgets
class EmbeddingNode(ProjectNode):
    def __init__(self, embedding):
        super(EmbeddingNode, self).__init__(embedding)
        self._embedTab = None

    def openImportWindow(self, parent):
        dial = EmbedImportDialog(parent)
        files = dial.getFiles()
        if files:
            loadFile, plugFile, k1, k2, k3, cat, reverse, openFile, shortFile = files
            samples = list()
            if reverse == ReverseState.REVERSE:
                openSample = self._dataObject.importOpen(openFile)
                shortSample = self._dataObject.importShort(shortFile)
                samples.extend([openSample, shortSample])
            plugProject = self._dataObject.importPlug(plugFile)
            pk1, pk2, pk3 = plugProject.getConstants()
            if not (k1 == pk1 and k2 == pk2 and k3 == pk3):
                plugProject.setConstants(k1, k2, k3)
                plugProject.recalculate()
            loadSample = self._dataObject.importLoad(loadFile, reverse, cat)
            samples.append(loadSample)
            if self._embedTab:
                self._embedTab.createTabs(reverse)
                self._embedTab.updateWidget()
            self.updateChildren()

    def addChildren(self, samples, plug, side):
        node = self.hasChild(side)
        if not node:
            node = Node(side)
            self.appendRow(node)
        if plug:
            node.appendRow(PlugNode(plug))
        for sample in samples:
            node.appendRow(SampleNode(sample, self._dataObject))

    def updateChildren(self):
        self.removeRow(0)
        if self._dataObject.plug():
            self.insertRow(0, PlugNode(self._dataObject.plug()))
        for side in self._dataObject.load():
            node = self.hasChild(side)
            if not node:
                node = Node(side)
                self.appendRow(node)
            node.setRowCount(0)
            if self._dataObject.load()[side]:
                node.appendRow(SampleNode(self._dataObject.load()[side], self._dataObject))
            if side == "Reverse":
                if self._dataObject.shortSample():
                    shortNode = Node("Short")
                    node.appendRow(shortNode)
                    shortNode.appendRow(SampleNode(self._dataObject.shortSample(), self._dataObject))
                if self._dataObject.openSample():
                    openNode = Node("Open")
                    node.appendRow(openNode)
                    openNode.appendRow(SampleNode(self._dataObject.openSample(), self._dataObject))

    def setupInitialData(self):
        self.updateChildren()

    def getWidgets(self, vnaManager):
        if not self._embedTab:
            self._embedTab = EmbedWidget(self, vnaManager)
        tabs = dict()
        tabs["Embedding"] = self._embedTab

        return tabs

    def setStandard(self, standard):
        super(EmbeddingNode, self).setStandard(standard)
        if self._embedTab:
            self._embedTab.createTabs(self._embedTab.getSide())
            self._embedTab.updateWidget()