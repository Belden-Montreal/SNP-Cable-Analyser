from collections import OrderedDict
class Standard():
    def __init__(self, name):
        self.name = name
        self.limits = OrderedDict({"RL":"", "IL":"", "NEXT":"", "PSNEXT":"","FEXT":"", "PSFEXT":"", "ACRF":"", "PSACRF":"", "LCL" : "", "LCTL" : "", "TCL" : "", "TCTL" : "", "ELTCTL" : "","CMRL" : "", "CMNEXT" : ""})

    def limit(self, index):
        if index < len(self.limits):
            return list(self.limits.values())[index]
        return ""