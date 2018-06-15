from sample.sample import Sample
from parameters.parameter_factory import ParameterFactory

class SingleEnded(Sample):
    '''
    This class contains the measurements for a single-ended connection, ie a plug
    '''
    def __init__(self, snpFile):
        super(SingleEnded, self).__init__(snpFile)

    def addParameters(self):
        parameters = [
            "RL",
            "NEXT",
            "Propagation Delay",
            "PSNEXT",
            "LCL",
            "TCL",
            "CMRL",
            "CMNEXT",
            "CMDMNEXT",
            "CMDMRL",
            "DMCMNEXT",
            "DMCMRL"
        ]

        for parameter in parameters:
            self._parameters[parameter] = self._factory.getParameter(parameter)

        
