from enum import Enum

class DataFormat(Enum):
    MAGNITUDE = ("Magnitude", "dB")
    PHASE     = ("Phase", "\u00b0")
    REAL      = ("Real", "TODO")
    IMAGINARY = ("Imaginary", "TODO")
    DELAY     = ("Delay", "s")

    def __init__(self, name, unit):
        self._name = name
        self._unit = unit

    def getName(self):
        return self._name

    def getUnit(self):
        return self._unit

    def getTitle(self):
        return "{} ({})".format(self._name, self._unit)

    
def formatParameterData(parameter, serie, pformat):
    data = None
    if pformat == DataFormat.MAGNITUDE:
        data = [mag for (mag,_) in parameter.getParameter()[serie]]
    if pformat == DataFormat.PHASE:
        data = [phase for (_,phase) in parameter.getParameter()[serie]]
    if pformat == DataFormat.REAL:
        data = [value.real for value in parameter.getComplexParameter()[serie]]
    if pformat == DataFormat.IMAGINARY:
        data = [value.imag for value in parameter.getComplexParameter()[serie]]
    if pformat == DataFormat.DELAY:
        data = [value.real for value in parameter.getComplexParameter()[serie]]
    return data
