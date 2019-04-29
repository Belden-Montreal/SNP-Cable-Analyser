from snpanalyzer.config.json import JSONConfiguration
from overrides import overrides

class VNAConfiguration(JSONConfiguration):
    def __init__(self):
        # set default value
        self.__address    = "TCPIP0::10.29.48.46::hislip0::INSTR"
        self.__bandwidth  = 300
        self.__minfreq    = 10000000
        self.__maxfreq    = 500000000
        self.__resolution = 1000
        self.__timeout    = 500000
        self.__average    = 1
        self.__testname   = "sample"
        self.__ports      = 8

    def setAddress(self, address):
        self.__address = address

    def getAddress(self):
        """
        The address of the VNA.
        """
        return self.__address

    def setBandwidth(self, bandwidth):
        self.__bandwidth = bandwidth

    def getBandwidth(self):
        return self.__bandwidth

    def setMinimumFrequency(self, minfreq):
        if minfreq > self.__maxfreq:
            return
        self.__minfreq = minfreq

    def getMinimumFrequency(self):
        """
        The minimum frequency to scan.
        """
        return self.__minfreq
        
    def setMaximumFrequency(self, maxfreq):
        if maxfreq < self.__minfreq:
            return
        self.__maxfreq = maxfreq

    def getMaximumFrequency(self):
        """
        The maximum frequency to scan.
        """
        return self.__maxfreq

    def setFrequencies(self, frequencies):
        (minfreq, maxfreq) = frequencies
        if minfreq > maxfreq:
            return
        self.__minfreq = minfreq
        self.__maxfreq = maxfreq

    def getFrequencies(self):
        """
        The frequencies range of the VNA (min, max).
        """
        return (self.__minfreq, self.__maxfreq)

    def setResolution(self, resolution):
        if resolution < 1:
            return
        self.__resolution = resolution

    def getResolution(self):
        """
        The number of points of the VNA.
        """
        return self.__resolution

    def setTimeout(self, timeout):
        if timeout < 0:
            return
        self.__timeout = timeout

    def getTimeout(self):
        """
        The timeout of the VNA.
        """
        return self.__timeout

    def setAverage(self, average):
        if average < 1:
            return
        self.__average = average

    def getAverage(self):
        """
        TODO: unknown.
        """
        return self.__average

    def setTestName(self, testname):
        self.__testname = testname
    
    def getTestName(self):
        """
        The number
        """
        return self.__testname

    def setNumberOfPorts(self, ports):
        if ports < 1:
            return
        self.__ports = ports

    def getNumberOfPorts(self):
        """
        The number of port to scan.
        """
        return self.__ports

    @overrides
    def toJSON(self):
        return {
            "bandwidth"  : self.getBandwidth(),
            "address"    : self.getAddress(),
            "minfreq"    : self.getMinimumFrequency(),
            "maxfreq"    : self.getMaximumFrequency(),
            "resolution" : self.getResolution(),
            "timeout"    : self.getTimeout(),
            "average"    : self.getAverage(),
            "testname"   : self.getTestName(),
            "ports"      : self.getNumberOfPorts(),
        }

    @staticmethod
    @overrides
    def fromJSON(json):
        vna = VNAConfiguration()
        vna.setBandwidth(json["bandwidth"])
        vna.setAddress(json["address"])
        vna.setMinimumFrequency(json["minfreq"])
        vna.setMaximumFrequency(json["maxfreq"])
        vna.setResolution(json["resolution"])
        vna.setTimeout(json["timeout"])
        vna.setAverage(json["average"])
        vna.setTestName(json["testname"])
        vna.setNumberOfPorts(json["ports"])
        return vna
        
