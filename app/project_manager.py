from project.project import Project
from project.plug import Plug
from project.alien import Alien
from project.embedding import Embedding
from app.save_manager import SaveManager

class ProjectManager(object):

    def __init__(self):
        self._projects = list()
        self._saveManager = SaveManager()

    def newProject(self, name):
        self._projects.append(Project(name))

    def newPlugProject(self, name):
        self._projects.append(Plug(name))

    def newAlienProject(self, name):
        self._projects.append(Alien(name))

    def newEmbeddingProject(self, name):
        self._projects.append(Embedding(name))
    
    def importFiles(self, parent, projectName):
        activeProject = self.getProjectByName(projectName)
        print(activeProject.getName())
        if activeProject:
            activeProject.openImportWindow(parent)

    def saveProject(self, name, projectName):
        activeProject = self.getProjectByName(projectName)
        if activeProject:
            self._saveManager.saveProject(name, activeProject)

    def loadProject(self, name):
        project = self._saveManager.loadProject(name)
        if project:
            self._projects.append(project)

    def getProjectByName(self, name):
        projects = [x for x in self._projects if x.getName() == name]
        if len(projects) == 1:
            return projects[0]

    def getProjects(self):
        return self._projects

    def deleteProjects(self, projectsNames):
        self._projects = [x for x in self._projects if x.getName() not in projectsNames]
