from embedding2 import Embedding
import re

class embeddingProject(Embedding):

    ''' This class uses the Embedding class to create a project composed of 
        multiple embedding instances'''

    def __init__(self, projectName):

        self.sampleList = []
        self.projectName = projectName

    def addSample(self):
        listOfSamples = self.getSampleListTestNames()
        #If the if a test by that name already exists, increment a number at the end of the sample name
        if testName in listOfSamples:
            reg = re.compile('_\d+$')
            idCount = reg.findall(testName)
            if idCount:
                IDNoCount = testName[0: 1-len(idCount[0])]
                print(IDNoCount)
                reg = re.compile('\d+$')
                num = reg.findall(idCount[0])
                nextCount = str(int(num[0]) + 1)

            else:
                IDNoCount = testName
                nextCount = "_1"

            self.addSample(IDNoCount + nextCount)
        else:
            self.sampleList.append(Embedding(testName))
            

    def getSampleListTestNames(self):
        listOfNames = []
        for item in self.sampleList:
            listOfNames.append(item.name)
        return listOfNames

 
if __name__ == '__main__':

    embProj = embeddingProject()
    embProj.addSample("123")
    embProj.addSample("123")
    embProj.addSample("123")
    embProj.addSample("123")
    embProj.addSample("123_17")

    print(embProj.getSampleListTestNames())

