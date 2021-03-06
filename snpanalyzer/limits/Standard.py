from collections import OrderedDict
from snpanalyzer.limits.Limit import Limit
parameters = ["RL", "IL", "_DELAY", "NEXT", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "ANEXT", "PSANEXT", "AVGPSANEXT", "AFEXT", "PSAFEXT", "PSAACRF", "AVGPSAACRF"]

class Standard():
    def __init__(self, name):
        self.name = name
        self.limits = OrderedDict()
        for param in parameters:
            self.limits[param] = Limit(param)
        
    def limit(self, index):
        if index < len(self.limits):
            return list(self.limits.values())[index]
        return ""

    def __str__(self):
        return self.name