from snpanalyzer.project.project import Project, ProjectNode
from snpanalyzer.sample.disturber import DisturberSample
from snpanalyzer.sample.victim import VictimSample
from snpanalyzer.gui.dialog.alien_import_dialog import AlienImportDialog
from snpanalyzer.parameters.type import ParameterType

from multiprocessing.dummy import Pool as ThreadPool
from copy import deepcopy

import xlsxwriter


class Alien(Project):
    '''
    The Alien class represents a project where multiple samples are disturbing a victim sample
    '''

    def __init__(self, name):
        super(Alien, self).__init__(name)
        self.type = "Alien"
        self._disturbers = dict()
        self._victims = dict()
        self._disturbers["PSANEXT"] = dict()
        self._disturbers["PSAACRF"] = dict()
        self._victims["PSANEXT"] = dict()
        self._victims["PSAACRF"] = dict()
        self._name = name
        for param in self._disturbers:
            self._disturbers[param]["End 1"] = list()
            self._disturbers[param]["End 2"] = list()
            self._victims[param]["End 1"] = None
            self._victims[param]["End 2"] = None


    def getSamples(self):
        samples= list()
        for param in self._disturbers:
            samples.append(self._victims[param]["End 1"])
            samples.append(self._victims[param]["End 2"])
        for param in self._disturbers:
            samples.extend(self._disturbers[param]["End 2"])
            samples.extend(self._disturbers[param]["End 1"])
        return samples
    def importSamples(self, fileNames, end, param, disturber=False):
        if disturber:
            pool = ThreadPool()
            samples = pool.starmap(self.__createDisturber, zip(fileNames, [param] * len(fileNames)))
            self._disturbers[param][end].extend(samples)
            if self._victims[param][end]:
                self._victims[param][end].setDisturbers(samples)
            return samples
        elif len(fileNames) < 2:
            for p in self._victims:
                for e in self._victims[p]:
                    sample = self.__createVictim(fileNames[0],e, p, self._disturbers[p][e])
                    self._victims[p][e] = sample
            return self._victims[param][end]

    def __createDisturber(self, name, param):
        return DisturberSample(name, remote=self.__isRemote(param), standard=self._standard)

    def __createVictim(self, name,end, param, disturbers):
        if self.__isRemote(param):
            strName= str(self._name+"Victim_REMOTE_"+end+".s16p")
        else:
            strName = str(self._name+"Victim_"+end+".s16p")
        return VictimSample(name, disturbers,strName=strName, remote=self.__isRemote(param), standard=self._standard)

    def __isRemote(self, name):
        return name == "PSAACRF"

    def removeSample(self, sample):
        for param in self._disturbers:
            for end in self._disturbers[param]:
                if sample in self._disturbers[param][end]:
                    self._disturbers[param][end].remove(sample)
                elif sample == self._victims[param][end]:
                    self._victims[param][end] = None

    def updateDisturbers(self, names, end, param):
        disturbers = [x for x in self._disturbers[param][end] if x.getName() in names]
        if self._victims[param][end]:
            self._victims[param][end].recalculate(disturbers)

    def resetDisturbers(self, end, param):
        if self._victims[param][end]:
            self._victims[param][end].resetDisturbers()

    def disturbers(self):
        return self._disturbers

    def victims(self):
        return self._victims

    def getType(self):
        return self.type

    def generateExcel(self, outputName, sampleNames, z=False):
        workbook = xlsxwriter.Workbook(outputName, options={'nan_inf_to_errors': True})

        for name, ends in self._victims.items():
            worksheet = workbook.add_worksheet(name)
            worksheet.write('A1', 'Alien ID:')
            worksheet.write('B1', self._name)

            cell_format = workbook.add_format({'align': 'center',
                                               'valign': 'vcenter',
                                               'border': 6, })
            worksheet.merge_range('A3:A5', "Frequency", cell_format)

            curPos = 1
            for end, sample in ends.items():
                if sample:
                    worksheet.merge_range(1, curPos, 1, curPos + sample.getNumPorts() * 2 - 1, end, cell_format)
                    for i, (paramName, parameter) in enumerate(sample.getParameters().items()):
                        paramName = str(paramName).replace("ParameterType.", "").replace("_", " ")

                        numSignals = 0
                        try:
                            if paramName in ["PSANEXT", "PSAFEXT", "PSAACRN", "PSAACRF"]:
                                numSignals = len(parameter.getPorts())
                                worksheet.merge_range(2, curPos, 2, curPos + numSignals - 1, paramName, cell_format)
                                param = parameter.getParameter()

                                for i, portName in enumerate(sorted(list(parameter.getDataSeries()), key=lambda
                                        params: params.getName())):  # enumerate(list(parameter.getDataSeries())):
                                    key = portName
                                    portName = portName.getName()

                                    worksheet.merge_range(3, curPos + i * 2, 3, curPos + i * 2 + 1, str(portName),
                                                          cell_format)
                                    # TODO: alien phase/complex values
                                    # if z:
                                    #     worksheet.write(4,curPos+i*2, "real", cell_format)
                                    #     worksheet.write(4,curPos+i*2+1, "imaginary", cell_format)
                                    #     param = parameter.getComplexParameter()

                                    #     for j,data in enumerate(param[key]):
                                    #         worksheet.write(5+j, 0, sample.getFrequencies()[j])
                                    #         self.box(workbook, worksheet, param, key, i*2, j, data.real, curPos)
                                    #         self.box(workbook, worksheet, param, key, i*2+1, j, data.imag, curPos)
                                    # else:
                                    worksheet.write(4, curPos + i * 2, "mag", cell_format)
                                    worksheet.write(4, curPos + i * 2 + 1, "phase", cell_format)
                                    param = parameter.getParameter()
                                    for j, (mag, phase) in enumerate(param[key]):
                                            worksheet.write(5 + j, 0, sample.getFrequencies()[j])
                                            self.box(workbook, worksheet, param, key, i * 2, j, mag, curPos)
                                            self.box(workbook, worksheet, param, key, i * 2 + 1, j, phase, curPos)
                        except AttributeError as e:
                            print(e)

                        curPos += numSignals
        workbook.close()

    def nodeFromProject(self):
        return AlienNode(self)

    def setStandard(self, standard):
        self._standard = standard
        for param in self._disturbers:
            for end in self._disturbers[param]:
                for disturber in self._disturbers[param][end]:
                    disturber.setStandard(standard)
                if self._victims[param][end]:
                    self._victims[param][end].setStandard(standard)

    def getCurrentAnalyses(self, param, end):
        v = self._victims[param][end]
        if v:
            if v.isRemote():
                ptype = ParameterType.PSAFEXT
                ptype2 = ParameterType.PSAACRF
            else:
                ptype = ParameterType.PSANEXT
                ptype2 = ParameterType.PSAACRN
            return v.getAnalysis(ptype), v.getAnalysis(ptype2)
        return None, None


from snpanalyzer.app.node import Node
from snpanalyzer.sample.sample import SampleNode
from snpanalyzer.gui.widget.alien_widget import AlienWidget
from PyQt5 import QtWidgets


class AlienNode(ProjectNode):
    def __init__(self, alien):
        super(AlienNode, self).__init__(alien)
        self._alienTab = None

    def openImportWindow(self, parent):
        dial = AlienImportDialog(parent)
        files = dial.getFiles()
        if files:
            disturbersFile, victimFile, end, param = files
            if disturbersFile:
                self._dataObject.importSamples(disturbersFile, end, param, disturber=True)
            if victimFile:
                self._dataObject.importSamples([victimFile], end, param, disturber=False)
            self.updateChildren()
            if self._alienTab:
                self._alienTab.updateWidget()


    def updateChildren(self):
        for param in self._dataObject.disturbers():
            node = self.hasChild(param)
            if not node:
                node = Node(param)
                self.appendRow(node)
            for end in self._dataObject.disturbers()[param]:
                subNode = node.hasChild(end)
                if not subNode:
                    subNode = Node(end)
                    node.appendRow(subNode)
                subNode.setRowCount(0)
                if self._dataObject.victims()[param][end]:
                    subNode.appendRow(SampleNode(self._dataObject.victims()[param][end], self._dataObject))
                if len(self._dataObject.disturbers()[param][end]) > 0:
                    disturbersNode = Node("Disturbers")
                    subNode.appendRow(disturbersNode)
                    for disturber in self._dataObject.disturbers()[param][end]:
                        disturbersNode.appendRow(SampleNode(disturber, self._dataObject))

    def setupInitialData(self):
        self.updateChildren()

    def getWidgets(self, vnaManager):
        if not self._alienTab:
            self._alienTab = AlienWidget(self, vnaManager)

        return {"Alien": self._alienTab}

    def setStandard(self, standard):
        self._dataObject.setStandard(standard)
        self._alienTab.updateWidget()
