from zipfile import ZipFile
import os
import xmltodict
import shutil
import dill
from project.project import Project

class SaveManager(object):

    # def __init__(self):
    #     pass

    def loadProject(self, fileName):
        with open(fileName, 'rb') as input:
            project = dill.load(input)
        return project

    def saveProject(self, fileName, project):
        with open(fileName, 'wb') as output:
            dill.dump(project, output)