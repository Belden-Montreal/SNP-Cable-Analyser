from enum import Enum

class FrequencyUnit(Enum):
    HERTZ     = ("Hz",  1e0)
    KILOHERTZ = ("kHz", 1e3)
    MEGAHERTZ = ("MHz", 1e6)
    GIGAHERTZ = ("GHz", 1e9)

    def __init__(self, unit, factor):
        self.__unit   = unit
        self.__factor = factor

    def getUnit(self):
        return self.__unit

    def getFactor(self):
        return self.__factor
