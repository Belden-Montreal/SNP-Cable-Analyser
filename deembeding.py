from snpAnalyze import SNPManipulations

class Deembeding(SNPManipulations):

    def getOpenDelay(self, openSNP):
        '''
        Using aquired S8P for an open sample, this function returns the progation delay
        on all pairs
        '''
        self.openSample = SNPManipulations(openSNP)

        return self.openSample.getPropagationDelay()
    

    def getShortDelay(self, openSNP):
        '''
        Using aquired S8P for a shorted sample, this function returns the progation delay
        on all pairs
        '''
        self.shortSample = SNPManipulations(shortSNP)

        return self.shortSample.getPropagationDelay()

    def calcDelay(self):
        
