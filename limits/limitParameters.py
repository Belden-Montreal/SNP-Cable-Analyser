from collections import OrderedDict
PARAMETERS = ["RL", "IL", "NEXT", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT"]
PARAMETERS_HEADER = OrderedDict({"RL" : "RL", "IL" : "IL", "NEXT" : "NEXT", "PSNEXT" : "PSNEXT","FEXT" : "FEXT", "PSFEXT" : "PSFEXT", "ACRF" : "ACRF", "PSACRF" : "PSACRF", "LCL" : "LCL", "LCTL" : "LCTL", "TCL" : "TCL", "TCTL" : "TCTL", "ELTCTL" : "ELTCTL","CMRL" : "CMRL", "CMNEXT" : "CMNEXT"})
class ParameterDict():
    def __init__(self, header):
        if not header:
            self.dict = OrderedDict({"RL":"", "IL":"", "NEXT":"", "PSNEXT":"","FEXT":"", "PSFEXT":"", "ACRF":"", "PSACRF":"", "LCL" : "", "LCTL" : "", "TCL" : "", "TCTL" : "", "ELTCTL" : "","CMRL" : "", "CMNEXT" : ""})
        else:
            self.dict = PARAMETERS_HEADER.copy()