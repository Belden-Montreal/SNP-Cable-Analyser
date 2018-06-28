from sample.sample import Sample, PORTS_NAME
from parameters.parameter_factory import ParameterFactory
class EndToEnd(Sample):

    def __init__(self, snpFile):
        super(EndToEnd, self).__init__(snpFile)

    def addParameters(self):
        parameters = [
            "RL",
            "IL",
            "NEXT",
            "Propagation Delay",
            "PSNEXT",
            "FEXT",
            "PSFEXT",
            "ACRF",
            "PSACRF",
            "LCL",
            "LCTL",
            "TCL",
            "TCTL",
            "ELTCTL",
            "CMRL",
            "CMNEXT",
            "CMDMNEXT",
            "CMDMRL",
            "DMCMNEXT",
            "DMCMRL"
        ]

        for parameter in parameters:
            self._parameters[parameter] = self._factory.getParameter(parameter)

    def setPorts(self):
        for i in range(self._portsNumber//2):
            self._ports[i] = (PORTS_NAME[i], False)
            self._ports[i+self._portsNumber//2] = ("(r)"+PORTS_NAME[i], True)
