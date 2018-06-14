from sample.sample import Sample
from parameters.parameter_factory import ParameterFactory

class SingleEnded(Sample):
    '''
    This class contains the measurements for a single-ended connection, ie a plug
    '''

    def __init__(self, snpFile):
        super(SingleEnded, self).__init__(snpFile)

    def addParameters(self):
        factory = ParameterFactory()
        parameters_name = ["RL", "NEXT", "Propagation Delay", "PSNEXT", "LCL", "TCL", "CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]
        for parameter in parameters_name:
            self._parameters[parameter] = factory.getParameter(parameter, self._ports, self._freq, self._mm, self._parameters)
        