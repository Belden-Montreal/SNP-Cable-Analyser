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

