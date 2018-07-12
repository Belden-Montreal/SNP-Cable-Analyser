from project.project import Project, ProjectNode
from project.plug import Plug, PlugNode
from project.alien import Alien, AlienNode
from project.embedding import Embedding, EmbeddingNode
from app.save_manager import SaveManager

class ProjectManager(object):

    def __init__(self):
        self._projects = list()
        self._saveManager = SaveManager()

    def newProject(self, name):
        project = Project(name)
        self._projects.append(project)
        return project.nodeFromProject()

    def newPlugProject(self, name):
        project = Plug(name)
        self._projects.append(project)
        return project.nodeFromProject()

    def newAlienProject(self, name):
        project = Alien(name)
        self._projects.append(project)
        return project.nodeFromProject()

    def newEmbeddingProject(self, name):
        project = Embedding(name)
        self._projects.append(project)
        return project.nodeFromProject()
    
    def importFiles(self, parent, activeProject):
        if activeProject:
            activeProject.openImportWindow(parent)

    def saveProject(self, name, activeProject):
        if activeProject:
            self._saveManager.saveProject(name, activeProject)

    def loadProject(self, name):
        project = self._saveManager.loadProject(name)
        if project:
            self._projects.append(project)
            return project.nodeFromProject()

    def getProjectByName(self, name):
        projects = [x for x in self._projects if x.getName() == name]
        if len(projects) == 1:
            return projects[0]

    def getProjects(self):
        return self._projects

    def deleteProjects(self, projects):
        self._projects = [x for x in self._projects if x.getName() not in [p.getName() for p in projects]]