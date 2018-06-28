from sample.sample import Sample, PORTS_NAME

class Victim(Sample):

    def __init__(self, snpFile, axextd):
        self._axextd = axextd
        super(Victim, self).__init__(snpFile)

    def addParameters(self):
        parameters = [
            "IL",
            "AXEXTD",
            "PSAXEXT",
            "PSAACRX",
        ]

        for parameter in parameters:
            if parameter == "AXEXTD":
                self._parameters[parameter] = self._axextd
            else:
                self._parameters[parameter] = self._factory.getParameter(parameter)

    def setPorts(self):
        for i in range(self._portsNumber//2):
            self._ports[i] = (PORTS_NAME[i], False)
            self._ports[i+self._portsNumber//2] = ("(d)"+PORTS_NAME[i], True)

    def setAxextd(self, axextd):
        self._axextd = axextd
        self.addParameters()