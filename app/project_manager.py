from project.project import Project
from project.plug import Plug
from project.alien import Alien
from project.embedding import Embedding
from app.save_manager import SaveManager

class ProjectManager(object):

    def __init__(self):
        self._projects = list()
        self._saveManager = SaveManager()

    def newProject(self, name, model):
        project = Project(name)
        self._projects.append(project)
        self.__addProjectToModel(model, project)

    def newPlugProject(self, name, model):
        project = Plug(name)
        self._projects.append(project)
        self.__addProjectToModel(model, project)

    def newAlienProject(self, name, model):
        project = Alien(name)
        self._projects.append(project)
        self.__addProjectToModel(model, project)

    def newEmbeddingProject(self, name, model):
        project = Embedding(name)
        self._projects.append(project)
        self.__addProjectToModel(model, project)
    
    def importFiles(self, parent, activeProject):
        if activeProject:
            activeProject.openImportWindow(parent)

    def saveProject(self, name, activeProject):
        if activeProject:
            self._saveManager.saveProject(name, activeProject)

    def loadProject(self, name, model):
        project = self._saveManager.loadProject(name, model)
        if project:
            self._projects.append(project)

    def getProjectByName(self, name):
        projects = [x for x in self._projects if x.getName() == name]
        if len(projects) == 1:
            return projects[0]

    def getProjects(self):
        return self._projects

    def deleteProjects(self, projects):
        self._projects = [x for x in self._projects if x.getName() not in [p.getName() for p in projects]]

    def __addProjectToModel(self, model, project):
        model.beginResetModel()
        model.rootItem.addChild(project.getTreeItem())
        model.endResetModel()