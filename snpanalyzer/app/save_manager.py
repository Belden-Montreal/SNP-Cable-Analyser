import dill
import os
import json
import xml.etree.cElementTree as ET
import shutil
import xmltodict
import pprint
import sys
from snpanalyzer.project.project import Project
from snpanalyzer.project.alien import Alien

class SaveManager(object):

    # def __init__(self):
    #     pass

    '''def loadProject(self, fileName):
        with open(fileName, 'rb') as input:
            project = dill.load(input)
        return project'''

    def loadProject(self, fileName):

        f = open(fileName, "r")
        f = f.read()
        projectDict = xmltodict.parse(f)

        for _, savedProj in projectDict["root"].items():
            projType = savedProj["@type"]
            projName = savedProj["@name"]
            del savedProj["@type"]
            del savedProj["@name"]
            if projType == "Other":
                project = Project(projName)
                #print(savedProj)
                for sample in savedProj["Sample"]:   
                    print(os.path.normpath(sample["file_name"]))
                    samples = project.importSamples([os.path.normpath(sample["file_name"])])
        return project

    '''def saveProject(self, fileName, project):
        with open(fileName, 'wb') as output:
            dill.dump(project, output)'''

    def saveProject(self, path, projects):
        folderName = path
        fileName = os.path.basename(path)
        os.mkdir(folderName)
        snpDir = os.path.join(folderName, "snps")
        os.mkdir(snpDir)

        #Create a new config file that will
        #contain all the sample settings of a given
        #project. This will include all the standards
        #and limits. 
        configurationPath = os.path.join(folderName, fileName + ".xml")

        for project in projects:
            #print(project)
            root = ET.Element("root")
            print(project.type)
            projectBranch = ET.SubElement(root, "Project", attrib = {"name" : str(project.getName()), "type": str(project.type)})

            configDict = {}
            configDict[fileName] = []
            if project.type == "Other":
                for sample in project.samples():
                    sampleBranch = ET.SubElement(projectBranch, "Sample")
                    ET.SubElement(sampleBranch, "name").text = str(sample.getName())
                    shutil.copy2(sample.getFileName(), os.path.join(snpDir, sample.getName())) # complete target filename given
                    ET.SubElement(sampleBranch, "file_name").text = str(os.path.join(snpDir, sample.getName()))
                    ET.SubElement(sampleBranch, "standard").text = str(sample.getStandard())

            if project.type == "Alien":
                pass

            if project.type == "Embedding":
                pass

        tree = ET.ElementTree(root)
        tree.write(configurationPath)     



