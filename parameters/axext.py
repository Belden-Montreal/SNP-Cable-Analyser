from parameters.parameter import PairedParameter, complex2db, order, diffDiffMatrix

class AXEXT(PairedParameter):
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
        self._il = il
        super(AXEXT, self).__init__(ports, freq, matrices)

    def computePairs(self, ports):
        # create each pair for the ANEXT
        pairs = dict()
        
        pairs.update(self._fext.getPairs())
        pairs.update(self._il.getPairs())

        return pairs

    def computeParameter(self):
        # initialize the dictionaries for each port
        (dbAXEXT, cpAXEXT) = (dict(), dict())
        dbIl = self._il.getParameter(full=True)
        cpIl = self._il.getComplexParameter(full=True)
        dbFext = self._fext.getParameter()
        cpFext = self._fext.getComplexParameter()
        
        # extract the ANEXT values from the fext and il
        dbAXEXT.update(dbFext)
        cpAXEXT.update(cpFext)
        dbAXEXT.update(dbIl)
        cpAXEXT.update(cpIl)        
        return (dbAXEXT, cpAXEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "AXEXT"
