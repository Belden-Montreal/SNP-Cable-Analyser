from snpanalyzer.project.project import Project, ProjectNode
from snpanalyzer.gui.dialog.embedding_import_dialog import EmbedImportDialog, ReverseState
from snpanalyzer.sample.delay import DelaySample
from snpanalyzer.sample.deembed import DeembedSample, ReverseDeembedSample
from snpanalyzer.parameters.type import ParameterType
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
        self.type = "Embedding"
        self.plugFileName = None #Quick patch to get XML File of the plug
        self.plugFile = None
    def getSamples(self):
        sample=list()
        if self._load["Reverse"]:
            sample.append(self._load["Reverse"])
        if self._open:
            sample.append(self._open)
        if self._short:
            sample.append(self._short)
        if self._load["Forward"]:
            sample.append(self._load["Forward"])
        return sample

    def importPlug(self, plugFile):
        from snpanalyzer.app.save_manager import SaveManager
        import os
        self._plug = SaveManager().loadProject(plugFile)
        self.plugFile  = plugFile
        self.plugFileName = os.path.basename(plugFile)
        print(self._plug.getSamples())
        return self._plug

    def importLoad(self, loadFile, side, cat="CAT5e"):
        if cat == "CAT5e":
            cases = Case.CAT5E
        else:
            cases = Case.CAT6
        if side == "Forward":
            self._load[side] = DeembedSample(loadFile, self._plug.getPlugNext(), self._plug.getNextDelay(), cases, standard=self._standard)
        else:
            print(side)
            k1, k2, k3 = self._plug.getConstants()
            self._load[side] = ReverseDeembedSample(loadFile, self._plug.getPlugNext(), self._plug.getPlugDelay(),
                                              self._open.getParameter(ParameterType.PROPAGATION_DELAY), self._short.getParameter(ParameterType.PROPAGATION_DELAY), k1, k2, k3, cases, standard=self._standard)
        return self._load[side]

    def getCaseF(self):
        return self._load["Forward"].getParameters()[ParameterType.CASE]

    def getCaseR(self):
        return self._load["Reverse"].getParameters()[ParameterType.RCASE]


    def importOpen(self, openFile):
        self._open = DelaySample(openFile)
        return self._open

    def importShort(self, shortFile):
        self._short = DelaySample(shortFile)
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

    def getType(self):
        return self.type

    def plug(self):
        return self._plug

    def generateExcel(self, outputName, sampleNames, z=False):
        workbook = xlsxwriter.Workbook(outputName, options={'nan_inf_to_errors': True})
        for side, sample in self._load.items():
            print(side, sample)
            if sample:
                worksheet = workbook.add_worksheet(side)
                worksheet.write('A1', 'De-embedding ID:')
                worksheet.write('B1', sample.getName())
            
                cell_format = workbook.add_format({'align': 'center',
                                                    'valign': 'vcenter',
                                                    'border': 6,})
                worksheet.merge_range('A3:A5', "Frequency", cell_format)

                curPos = 1
                #parameters = {"RL": sample.getParameters()["RL"], "NEXT": sample.getParameters()["NEXT"], "DNEXT": sample.getParameters()["DNEXT"], "Case": sample.getParameters()["Case"]}
                for i, (paramName, parameter) in enumerate(sample.getParameters().items()):
                    try:
                        numSignals = len(parameter.getParameter().keys())
                    except:
                        continue
                    paramName = str(paramName).replace("ParameterType.", "").replace("_", " ").split(":")[0]

                    if "DELAY" in paramName:
                        worksheet.merge_range(2, curPos, 2, curPos + numSignals - 1, paramName, cell_format)
                        for i, portName in enumerate(sorted(list(parameter.getDataSeries()), key=lambda
                                params: params.getName())):  # enumerate(list(parameter.getDataSeries())):
                            portSeries = portName
                            # print(parameter)
                            portName = portName.getName()
                            worksheet.write(3, curPos + i, str(portName), cell_format)
                            worksheet.write(4, curPos + i, "ns", cell_format)
                            param = parameter.getParameter()
                            try:
                                if type(param[portSeries]) is not list:
                                    param[portSeries] = [param[portSeries]]
                                for j, ns in enumerate(list(param[portSeries])):
                                    worksheet.write(5 + j, 0, sample.getFrequencies()[j])
                                    self.box(workbook, worksheet, param, portSeries, i, j, ns, curPos, line=True)

                            except Exception as e:
                                print(e)
                        curPos += numSignals
                    elif "CASE" in paramName:
                        cases = 0
                        activeCase= len([t for t,(a,b) in parameter.getCases().items() if b is not None])
                        worksheet.merge_range(1, curPos, 1, curPos + activeCase * 2 - 1, paramName, cell_format)
                        for i, portName in enumerate(
                            sorted(list(parameter.getDataSeries()), key=lambda params: params.getName())):
                            portSeries = portName
                            portName = portName.getName()
                            if z:
                                param = parameter.getComplexParameter()
                                ncp = len(param[portSeries].keys())

                                worksheet.merge_range(2, curPos + cases * 2, 2, curPos + cases*2 + ncp * 2 -1, str(portName), cell_format)

                                for x, c in enumerate(param[portSeries]):
                                    worksheet.merge_range(3, curPos+cases*2+x*2, 3, curPos+cases*2+x*2+1 ,"Case "+str(c),cell_format)
                                    worksheet.write(4, curPos+cases*2+x*2, "real", cell_format)
                                    worksheet.write(4, curPos+cases*2+x*2+1, "imaginary", cell_format)
                                    for j, data in enumerate(param[portSeries][c]):

                                            worksheet.write(5 + j, 0, sample.getFrequencies()[j])
                                            self.box(workbook, worksheet, param[portSeries], c, cases*2+x*2, j, data.real,
                                                         curPos,case=activeCase)
                                            self.box(workbook, worksheet, param[portSeries], c, cases*2+x*2+1, j, data.imag,
                                                         curPos,case=activeCase, line = True)

                            else:
                                param = parameter.getParameter()
                                ncp = len(param[portSeries].keys())

                                worksheet.merge_range(2, curPos + cases * 2, 2, curPos + cases * 2 + ncp * 2 - 1,
                                                      str(portName), cell_format)

                                for x, c in enumerate(param[portSeries]):
                                    worksheet.merge_range(3, curPos + cases * 2 + x * 2, 3,
                                                          curPos + cases * 2 + x * 2 + 1, "Case " + str(c), cell_format)
                                    worksheet.write(4, curPos + cases * 2 + x * 2, "mag", cell_format)
                                    worksheet.write(4, curPos + cases * 2 + x * 2 + 1, "phase", cell_format)
                                    for j, (mag,phase) in enumerate(param[portSeries][c]):
                                        worksheet.write(5 + j, 0, sample.getFrequencies()[j])
                                        self.box(workbook, worksheet, param[portSeries], c, cases * 2 + x * 2, j,
                                                 mag,
                                                 curPos, case=activeCase)
                                        self.box(workbook, worksheet, param[portSeries], c, cases * 2 + x * 2 + 1, j,
                                                 phase,
                                                 curPos, case=activeCase, line=True)
                            cases += ncp
                        curPos += activeCase * 2

                    else:
                        worksheet.merge_range(2, curPos, 2, curPos+numSignals*2-1,  paramName, cell_format)
                        for i, portName in enumerate(
                            sorted(list(parameter.getDataSeries()), key=lambda params: params.getName())):
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
                                    self.box(workbook, worksheet, param, portSeries, i * 2 + 1, j, data.imag, curPos, line=True)

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
                                        self.box(workbook, worksheet, param, portSeries, i * 2 + 1, j, phase,curPos, line=True)
                                except Exception as e:
                                    print(e)
                        curPos += numSignals * 2




        workbook.close()

    def box(self, workbook, worksheet, parameter, port, i, j, data, curPos, case= None, line= None):
        box_form = workbook.add_format()
        if line:
            box_form.set_right()
        if j == 0:
            box_form.set_top(6)
        if i == 0:
            box_form.set_left(6)
        if j == len(parameter[port])-1:
            box_form.set_bottom(6)
        if case:
            if i == case*2-1:
                box_form.set_right(6)
        else:
            if i == len(parameter)*2-1:
                box_form.set_right(6)


        if type(data) is not str:
            worksheet.write_number(j+5, curPos+i, data, box_form)
        else:
            worksheet.write(j+5, curPos+i, str(data), box_form)
        
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
        self._standard = standard
        for side in self._load.values():
            if side:
                side.setStandard(standard)


from snpanalyzer.app.node import Node
from snpanalyzer.sample.sample import SampleNode
from snpanalyzer.project.plug import PlugNode
from snpanalyzer.gui.widget.embed_widget import EmbedWidget
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
            if reverse == ReverseState.REVERSE:
                if openFile:
                    self._dataObject.importOpen(openFile)
                if shortFile:
                    self._dataObject.importShort(shortFile)
            if plugFile:
                plugProject = self._dataObject.importPlug(plugFile)
                pk1, pk2, pk3 = plugProject.getConstants()
                if not (k1 == pk1 and k2 == pk2 and k3 == pk3):
                    plugProject.setConstants(k1, k2, k3)
                    plugProject.recalculate()
            if loadFile:
                self._dataObject.importLoad(loadFile, reverse, cat)
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
            if side == "Reverse":
                if self._dataObject.shortSample():
                    shortNode = Node("Short")
                    node.appendRow(shortNode)
                    shortNode.appendRow(SampleNode(self._dataObject.shortSample(), self._dataObject))
                if self._dataObject.openSample():
                    openNode = Node("Open")
                    node.appendRow(openNode)
                    openNode.appendRow(SampleNode(self._dataObject.openSample(), self._dataObject))
            if self._dataObject.load()[side]:
                node.appendRow(SampleNode(self._dataObject.load()[side], self._dataObject))

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