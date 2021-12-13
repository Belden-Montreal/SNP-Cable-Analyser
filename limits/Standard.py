from collections import OrderedDict
from limits.Limit import Limit
parameters =  []
class Standard():
    def __init__(self, name, type=None):
        self.name = name
        self.limits = OrderedDict()

        if type == "Embedding":
            self.parameters = ["Mat. Next", "Mat. Next 1,4", "TPMag 45-36 L", "TPMag 45-36 H", "TPMag 12-36 L", "TPMag 12-36 H", "TPMag 36-78 L", "TPMag 36-78 H", "TPMag 36-78 L", "TPMag 36-78 L", "TPMag 45-12 L", "TPMag 45-12 H", "TPMag 45-78 L", "TPMag 45-78 H", "TPMag 12-78 L", "TPMag 12-78 H", "TPPhase 45-36 L", "TPPhase 45-36 H", "TPPhase 12-36 L", "TPPhase 12-36 H", "TPPhase 36-78 L", "TPPhase 36-78 H", "TPPhase 36-78 L", "TPPhase 36-78 L", "TPPhase 45-12 L", "TPPhase 45-12 H", "TPPhase 45-78 L", "TPPhase 45-78 H", "TPPhase 12-78 L", "TPPhase 12-78 H"]
        else:
            self.parameters= ["RL", "IL", "PropagationDelay", "NEXT", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL", "ANEXT", "PSANEXT", "AVGPSANEXT", "AFEXT", "PSAFEXT", "PSAACRF", "AVGPSAACRF"]
        for param in self.parameters:
            self.limits[param] = Limit(param, type=type)
       
    def limit(self, index):
        if index < len(self.limits):
            return list(self.limits.values())[index]
        return ""

    def __str__(self):
        return self.name