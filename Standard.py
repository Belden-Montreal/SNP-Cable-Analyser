class Standard():

    def __init__(self, sampleObject, standard = None):

        limit = Limit(sampleObject,standard) #The Limit class contains all the limits for the parameters
                                             #By passing the sampleObject, the limit class is able to perform calculations
                                             #that may depend on the measured values.
    def loadFromXML(self):
        pass

    @property
    
