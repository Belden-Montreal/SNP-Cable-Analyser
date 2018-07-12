from parameters.parameter import Parameter, complex2db, order, diffDiffMatrix

class AXEXT(Parameter):
    """
    The AXEXT parameter can either represent the ANEXT or the AFEXT.

    The following setup can be used for measuring the ANEXT:

        measurement (disturbed) [ ]----------------[x] terminator
        measurement (disturber) [ ]----------------[x] terminator

    The following setup can be used for measuring the AFEXT:

        measurement (disturbed) [ ]----------------[x] terminator
                     terminator [x]----------------[ ] measurement (disturber)

    In both case, the main ports of the configuration should contains the
    measurements of the disturbed and the remote ports of the configuration
    should contains the measurements of the disturber.

    Using this port configuration on 4 twisted pairs cables, we get the
    equivalent network:

                           -----------------
            disturbed 1 ---|               |--- disturber 1
            disturbed 2 ---|               |--- disturber 2
            disturbed 3 ---|               |--- disturber 3
            disturbed 4 ---|               |--- disturber 4
                           -----------------

    In ANEXT or AFEXT, each disturber port affects each disturbed port. This
    means that either parameter has 16 data series in the network above. Using
    the equivalent network above, the calculations can be done by reusing
    other parameters:

        - 12 of these data series are equivalent to a normal FEXT
        -  4 of these data series are equivalent to a normal insertion loss
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
