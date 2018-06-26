from project.project import Project
from project.plug import Plug
from project.alien import Alien
from project.embedding import Embedding

class ProjectManager(object):

    def __init__(self):
        self._activeProject = None

    def newProject(self, name):
        self._activeProject = Project()

    def newPlugProject(self, name):
        self._activeProject = Plug()

    def newAlienProject(self, name):
        self._activeProject = Alien()

    def newEmbeddingProject(self, name):
        self._activeProject = Embedding()
    
    def importFiles(self, parent):
        if self._activeProject:
            self._activeProject.openImportWindow(parent)

    def activeProject(self):
        return self._activeProject

    def saveProject(self):
        pass
        #self._activeProject.save()

    def loadProject(self):
        pass