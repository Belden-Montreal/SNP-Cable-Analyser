from project.project import Project
from sample.disturber import Disturber
from sample.victim import Victim
from app.component_tree_item import ComponentTreeItem
from project.alien_import_dialog import AlienImportDialog
from project.subproject import Subproject
from multiprocessing.dummy import Pool as ThreadPool


class Alien(Project):
    '''
    The Alien class represents a project where multiple samples are disturbing a victim sample
    '''
    def __init__(self, name):
        self._ends = dict()
        self._ends["end1"] = Subproject("End 1")
        self._ends["end2"] = Subproject("End 2")
        for end in self._ends.values():
            end.addComponent(Subproject("ANEXT"))
            end.addComponent(Subproject("AFEXT"))
        super(Alien, self).__init__(name)
        self._victim = None
        self._disturbers = list()
        self._axextd = None
        

    def importSamples(self, fileNames, disturber=False):
        if disturber:
            pool = ThreadPool()
            samples = pool.map(self.__createDisturber, fileNames)
            self._disturbers.extend(samples)
            self._samples.extend(samples)
            self._axextd = self.calculateAXEXTD()
            if self._victim:
                self._victim.setAxextd(self._axextd)
        elif len(fileNames) < 2:
            if len(self._disturbers):
                self._victim = self.__createVictim(fileNames[0], self._axextd)
                self._samples.append(self._victim)
            else:
                print("can't import victim before disturbers")
        else:
            print("can't import multiple victims")

    def calculateAXEXTD(self):
        return [disturber.getParameters()["AXEXT"] for disturber in self._disturbers]

    def removeSamples(self, names):
        super(Alien, self).removeSamples(names)
        if len(names) > 0:
            if self._victim.getName() in names:
                self._victim = None

            self._disturbers = [x for x in self._disturbers if x.getName() not in names]

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def openImportWindow(self, parent):
        dial = AlienImportDialog(parent)
        disturbers, victim = dial.getFiles()
        self.importSamples(disturbers, disturber=True)
        self.importSamples([victim], disturber=False)
        component = next((comp for comp in self._ends["end1"].getComponents() if comp.getName() == "ANEXT"), None)
        component.setComponents(self._samples)
        self._generateTreeStructure()


    def _generateTreeStructure(self):
        self._treeItem.children = list()
        for end in self._ends.values():
            self._treeItem.addChild(end.getTreeItem())

    def __createDisturber(self, name):
        return Disturber(name)

    def __createVictim(self, name, axextd):
        return Victim(name, axextd)