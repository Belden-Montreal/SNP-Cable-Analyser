from project.project import Project
from project.plug import Plug
from project.alien import Alien
from project.embedding import Embedding
from app.save_manager import SaveManager

class ProjectManager(object):

    def __init__(self):
        self._activeProject = None
        self._saveManager = SaveManager()

    def newProject(self, name):
        self._activeProject = Project(name)

    def newPlugProject(self, name):
        self._activeProject = Plug(name)

    def newAlienProject(self, name):
        self._activeProject = Alien(name)

    def newEmbeddingProject(self, name):
        self._activeProject = Embedding(name)
    
    def importFiles(self, parent):
        if self._activeProject:
            self._activeProject.openImportWindow(parent)

    def activeProject(self):
        return self._activeProject

    def setActiveProject(self, project):
        self._activeProject = project

    def saveProject(self, name):
        self._saveManager.saveProject(name, self._activeProject)

    def loadProject(self, name):
        self._activeProject = self._saveManager.loadProject(name)