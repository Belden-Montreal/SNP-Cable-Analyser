from parameters.parameter import Parameter, complex2db, order, diffDiffMatrix

class AXEXT(Parameter):
    """
        AXEXT represents both the ANEXT and the AFEXT.
        It is calculated by taking both the FEXT and the Insertion Loss of the disturbed hardware
        
        For ANEXT measurements, the measurements must be done on the same side :

        measurement (disturbed) []------            --------//[]
                                        |           |
                                         -----------
                                         -----------
                                        |           |
        measurement (disturber) []------            --------//[]

        For AFEXT measurements, the measurements must be done on the opposite side :

        measurement (disturbed) []------            --------//[]
                                        |           |
                                         -----------
                                         -----------
                                        |           |
                               []//------            --------[] measurement (disturber) 
    """

    def __init__(self, ports, freq, matrices, fext, il):
        self._fext = fext
        self._il   = il
        super(AXEXT, self).__init__(ports, freq, matrices)

    def computeDataSeries(self):
        return self._fext.getDataSeries().union(self._il.getDataSeries())

    def computeParameter(self):
        # initialize the dictionaries for each port
        (dbAXEXT, cpAXEXT) = (dict(), dict())

        # get the parameters
        dbIL   = self._il.getParameter()
        cpIL   = self._il.getComplexParameter()
        dbFEXT = self._fext.getParameter()
        cpFEXT = self._fext.getComplexParameter()
        
        # extract the ANEXT values from the fext and il
        dbAXEXT.update(dbFEXT)
        cpAXEXT.update(cpFEXT)
        dbAXEXT.update(dbIL)
        cpAXEXT.update(cpIL)        
        return (dbAXEXT, cpAXEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "AXEXT"
