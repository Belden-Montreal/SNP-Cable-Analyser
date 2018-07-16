from sample.sample import Sample, PORTS_NAME

class Victim(Sample):

    def __init__(self, snpFile, param="ANEXT", disturbers=list()):
        self._axextd = [disturber.getParameters()[param] for disturber in disturbers]
        self._param = param
        if self._param == "ANEXT":
            self._psaxext = "PSANEXT"
            self._psaacrx = "PSAACRN"
        else:
            self._psaxext = "PSAFEXT"
            self._psaacrx = "PSAACRF"
        super(Victim, self).__init__(snpFile)

    def addParameters(self):
        parameters = [
            "IL",
            self._param+"D",
            self._psaxext,
            self._psaacrx,
        ]

        for parameter in parameters:
            if parameter == self._param+"D":
                self._parameters[parameter] = self._axextd
            else:
                self._parameters[parameter] = self._factory.getParameter(parameter)

    def setPorts(self):
        for i in range(self._portsNumber//2):
            self._ports[i] = (PORTS_NAME[i], False)
            self._ports[i+self._portsNumber//2] = ("(d)"+PORTS_NAME[i], True)

    def calculateAXEXTD(self, disturbers):
        self._axextd = [disturber.getParameters()[self._param] for disturber in disturbers]
        self._parameters["PS"+self._param].recalculate(self._axextd)
        if self._param == "ANEXT":
            name = "N"
        else:
            name = "F"
        self._parameters["PSAACR"+name].recalculate(self._parameters["PS"+self._param])
