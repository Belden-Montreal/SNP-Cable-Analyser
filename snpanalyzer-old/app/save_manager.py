import dill
import os
import json
import xml.etree.cElementTree as ET
import shutil
from distutils.dir_util import copy_tree
import xmltodict
import pprint
import sys
from snpanalyzer.project.project import Project
from snpanalyzer.project.plug import Plug
from snpanalyzer.project.alien import Alien
from snpanalyzer.project.embedding import Embedding

from collections import OrderedDict 

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
        #print(dict(projectDict["root"]))

        for _, savedProj in projectDict["root"].items():
            savedProj = savedProj
            print("projType : ", savedProj)
            projType = dict(savedProj)["@type"]
            print("projType : ", projType)

            projName = savedProj["@name"]
            del savedProj["@type"]
            del savedProj["@name"]
            if projType == "Other":
                project = Project(projName)
                print(savedProj)
                for _, items in savedProj.items():  
                    for sample in items:
                        print(sample) 
                        #print(os.path.normpath(sample["file_name"]))
                        samples = project.importSamples([os.path.normpath(sample["file_name"])])

            if projType == "Alien":
                project = Alien(projName)
                for key, sample in savedProj.items():
                    if key == "Victim":
                        disturber = False
                    else:
                        disturber = True
                    project.importSamples(fileNames = [os.path.normpath(sample[0]["file_name"])],
                                          end = sample[0]["@end"],
                                          param = sample[0]["@powerSum"],
                                          disturber=disturber)

            if projType == "Plug":
                project = Plug(projName)
                #project.setConstants(k1, k2, k3)
                print("DFOPEN FILE ", savedProj["Plug"]["dfOpen"])
                project.importDfOpen(os.path.normpath(savedProj["Plug"]["dfOpen"]))
                project.importDfShort(os.path.normpath(savedProj["Plug"]["dfShort"]))
                project.importOpen(os.path.normpath(savedProj["Plug"]["openSample"]))
                project.importShort(os.path.normpath(savedProj["Plug"]["shortSample"]))
                project.importLoad(os.path.normpath(savedProj["Plug"]["loadSample"]))
                k1 = savedProj["Plug"]["k1"]
                k2 = savedProj["Plug"]["k2"]
                k3 = savedProj["Plug"]["k3"]

                project.setConstants(k1,k2,k3)


            if projType == "Embedding":
                project = Embedding(projName)
                print(savedProj)
                #load plug file
                try:
                    project.importPlug(os.path.normpath(savedProj["Plug"]["file_name"]))
                except:
                    pass
                try:
                    project.importLoad(os.path.normpath(savedProj["Load_Forward"]["file_name"]),side = "Forward")
                except Exception as e:
                    print(e)


                try:
                    project.importOpen(os.path.normpath(savedProj["Open"]["file_name"]))
                except:
                    pass
                try:
                    project.importShort(os.path.normpath(savedProj["Short"]["file_name"]))
                except:
                    pass
                try:
                    project.importOpen(os.path.normpath(savedProj["Open"]["file_name"]))
                except:
                    pass
                try:
                    project.importShort(os.path.normpath(savedProj["Short"]["file_name"]))
                except:
                    pass
                try:
                    print(savedProj["Load_Reverse"])
                    project.importLoad(os.path.normpath(savedProj["Load_Reverse"]["file_name"]),side = "Reverse")
                except Exception as e:
                    print(e)
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
        print("Projects : ", projects)
        for project in projects:
            #print(project)
            root = ET.Element("root")
            print(project)
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
                #Save victim
                print(project.victims())
                for powerSum in project.victims():
                    for end in (project.victims())[powerSum]:
                        sample = (project.victims())[powerSum][end]
                        victimBranch = ET.SubElement(projectBranch, "Victim", attrib = {"powerSum" : powerSum, "end": end})
                        ET.SubElement(victimBranch, "name").text = str(sample.getName())
                        ET.SubElement(victimBranch, "file_name").text = str(os.path.join(snpDir, sample.getName()))
                        ET.SubElement(victimBranch, "standard").text = str(sample.getStandard())
                        shutil.copy2(sample.getFileName(), os.path.join(snpDir, sample.getName())) # complete target filename given

                for powerSum in project.disturbers():
                    for end in (project.disturbers())[powerSum]:
                        for sample in (project.disturbers())[powerSum][end]:
                            sampleBranch = ET.SubElement(projectBranch, "Disturber", attrib = {"powerSum" : powerSum, "end": end})
                            print(sample.getFileName()) 
                            ET.SubElement(sampleBranch, "name").text = str(sample.getName())
                            ET.SubElement(sampleBranch, "file_name").text = str(os.path.join(snpDir, sample.getName()))
                            ET.SubElement(sampleBranch, "standard").text = str(sample.getStandard())
                            shutil.copy2(sample.getFileName(), os.path.join(snpDir, sample.getName())) # complete target filename given





            if project.type == "Embedding":
                sampleBranch = ET.SubElement(projectBranch, "Plug")
                print("snpDir" , snpDir)
                ET.SubElement(sampleBranch, "file_name").text =  str(os.path.join(snpDir, project.plugFileName))
                print("new Location : ", str(os.path.join(snpDir, project.plugFileName)))
                #shutil.copy2(project.plugFile, os.path.join(snpDir, project.plug().getName())) # complete target filename given
                copy_tree(os.path.dirname(project.plugFile), snpDir) # complete target filename given

                #save load files  (Fwd, Rev)
                for side in project.load():
                    sample = project.load()[side]
                    if sample is not None:                    
                        sampleBranch = ET.SubElement(projectBranch, "Load_"+side)
                        ET.SubElement(sampleBranch, "file_name").text = str(os.path.join(snpDir, sample.getName()))
                        shutil.copy2(sample.getFileName(), os.path.join(snpDir, sample.getName())) # complete target filename given

                #save open file
                sampleBranch = ET.SubElement(projectBranch, "Open")
                sample = project.openSample()
                if sample is not None:
                    ET.SubElement(sampleBranch, "file_name").text = str(os.path.join(snpDir, sample.getName()))
                    shutil.copy2(sample.getFileName(), os.path.join(snpDir, sample.getName())) # complete target filename given

                #save short file
                sampleBranch = ET.SubElement(projectBranch, "Short")
                sample = project.shortSample()
                if sample is not None:
                    ET.SubElement(sampleBranch, "file_name").text = str(os.path.join(snpDir, sample.getName()))
                    shutil.copy2(sample.getFileName(), os.path.join(snpDir, sample.getName())) # complete target filename given

            if project.type == "Plug":
                samples = [project.dfOpen, 
                           project.dfShort,
                           project.openSample,
                           project.shortSample,
                           project.loadSample
                           ]
                sampleBranch = ET.SubElement(projectBranch, "Plug")
                for sample in samples:
                    shutil.copy2(sample().getFileName(), os.path.join(snpDir, sample().getName())) # complete target filename given
                    ET.SubElement(sampleBranch, sample.__name__).text = str(os.path.join(snpDir, sample().getName()))
                ET.SubElement(sampleBranch, "k1").text = str(project.getConstants()[0])
                ET.SubElement(sampleBranch, "k2").text = str(project.getConstants()[1])
                ET.SubElement(sampleBranch, "k3").text = str(project.getConstants()[2])
            
            










            #root.append(projectBranch)

        tree = ET.ElementTree(root)
        tree.write(configurationPath)     




