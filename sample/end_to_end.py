from sample.sample import Sample, PORTS_NAME
from parameters.parameter_factory import ParameterFactory
class EndToEnd(Sample):

    def __init__(self, snpFile):
        super(EndToEnd, self).__init__(snpFile)

    def addParameters(self):
        factory = ParameterFactory()
        parameters_name = ["RL", "IL", "NEXT", "Propagation Delay", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]
        for parameter in parameters_name:
            self._parameters[parameter] = factory.getParameter(parameter, self._ports, self._freq, self._mm, self._parameters)

    def setPorts(self):
        for i in range(self._portsNumber//2):
            self._ports[i] = PORTS_NAME[i]
            self._ports[i+self._portsNumber//2] = "(r)"+PORTS_NAME[i]