from typing import Set
from snpAnalyze import SNPManipulations
import os
from os.path import splitext
import time
import numpy as np

from settings import Settings

from genericworker import GenericWorker
from PyQt5 import QtCore     
from pathos.pools import ProcessPool
from multiprocessing import cpu_count
import time
class Sample(SNPManipulations):

    '''This class handles the SNP samples for the basic test'''

    def __init__(self, snpFile, one_sided = None, standard = None, fromPort = None, toPort = None, pair_names = None):

        self.settings = Settings()
        self.snpFile = snpFile

        self.rs = super(Sample, self)
        self.rs.__init__(self.snpFile)
        #self.renumber(renumFrom, renumTo)
        #self.portNumbering = toPort
        self.s2mm()

        self.portNumbering = []
        '''if (fromPort is None and toPort is None):
            for port in range(0, self.num_ports):
                self.portNumbering.append(port)
        else:
            self.portNumbering = toPort
            try:
                self.renumber(list(fromPort), list(toPort))
            except Exception:
                self.portNumbering = fromPort
                raise "Error:No Good"'''

        print("Converted")
        self.port_name = {0:"12", 1:"36", 2:"45", 3:"78"}

        print("NAME = ", snpFile)
        
        self.name, self.extension = splitext(os.path.basename(snpFile))
        self.date = time.ctime(os.path.getctime(snpFile))
        #print self.date

        self.standard = standard
        self.num_ports_dd = self.getNumPorts(self.dd)

        if one_sided != None:
            self.one_sided = one_sided
        
        elif self.num_ports_dd == 4: #Assume that the test is one-sided.
                                             #This can be changed
            self.one_sided = True

        elif self.num_ports_dd == 8: #Assume that test is end to end.
            self.one_sided = False

        self.port_name = {}

        if pair_names is None:
            self.pair_combo = self.settings.pairNames[:self.num_ports_dd] #["45", "12","36","78"]
        
        else:
            self.pair_combo = pair_names

        self.port_name = self.pair_combo
        if self.one_sided:
            #for i in range(0, self.num_ports_dd):
                #self.port_name[i] = self.pair_combo[i]  #{0:"45", 1:"12", 2:"36", 3:"78"}
            self.parameters = ["RL", "NEXT", "Propagation Delay", "PSNEXT", "LCL", "TCL", "CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]
        else:
            #for i in range(0, self.num_ports_dd//2):
                #self.port_name[i] = self.pair_combo[i]  #{0:"45", 1:"12", 2:"36", 3:"78"}
            #for i in range((self.num_ports_dd//2), self.num_ports_dd):
                #self.port_name[i] = "(r)"+self.pair_combo[i-self.num_ports_dd//2]  #{4:"(r)12",  :"(r)36", 6:"(r)45", 7:"(r)78", 0:"12", 1:"36", 2:"45", 3:"78"}
            self.parameters = ["RL", "IL", "NEXT", "Propagation Delay", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]
        
        self.worstValue = {}
        self.worstMargin = {}

        # self.getParameters()
        

    def getParameters(self):
        z=False
        self.RL = self.getRL(self.dd, z)
        self.IL = self.getIL(self.dd, z )
        self.NEXT = self.getNEXT(self.dd, z)
        self.PropagationDelay = self.getPropagationDelay()

        self.FEXT = self.getFEXT(self.dd, z)
        self.PSNEXT = self.getPSNEXT(self.dd)
        self.PSFEXT = self.getPSFEXT(self.dd)
        self.ACRF = self.getACRF(self.dd)
        self.PSACRF = self.getPSACRF(self.dd)

        self.LCL = self.getRL(self.dc, z)
        self.LCTL = self.getIL(self.dc, z)
        self.TCL = self.getRL(self.cd, z)
        self.TCTL = self.getIL(self.cd, z)
        self.ELTCTL = self.getELTCTL()

        self.CMRL =  self.getRL(self.cc, z) #commun mode Return Loss
        self.CMNEXT =  self.getNEXT(self.cc, z) #commun mode NEXT

        self.CMDMNEXT =  self.getNEXT(self.cd, z) #commun mode NEXT
        self.CMDMRL =  self.getRL(self.cd, z) #commun mode NEXT

        self.DMCMNEXT    = self.getNEXT(self.dc, z)
        self.DMCMRL      = self.getRL(self.dc, z)
        #print self.RL.keys()

        
        #real and complex values
        self.RLZ = self.getRL(self.dd)
        self.ILZ = self.getIL(self.dd)
        self.NEXTZ = self.getNEXT(self.dd)
        self.PropagationDelayZ = self.getPropagationDelay()

        self.FEXTZ = self.getFEXT(self.dd)
        self.PSNEXTZ = self.getPSNEXT(self.dd)
        self.PSFEXTZ = self.getPSFEXT(self.dd)
        self.ACRFZ = self.getACRF(self.dd)
        self.PSACRFZ = self.getPSACRF(self.dd)

        self.LCLZ = self.getRL(self.dc)
        self.LCTLZ = self.getIL(self.dc)
        self.TCLZ = self.getRL(self.cd)
        self.TCTLZ = self.getIL(self.cd)
        self.ELTCTLZ = self.getELTCTL()

        self.CMRLZ =  self.getRL(self.cc) #commun mode Return Loss
        self.CMNEXTZ =  self.getNEXT(self.cc) #commun mode NEXT

        self.CMDMNEXTZ =  self.getNEXT(self.cd) #commun mode NEXT
        self.CMDMRLZ =  self.getRL(self.cd) #commun mode NEXT

        self.DMCMNEXTZ    = self.getNEXT(self.dc)
        self.DMCMRLZ      = self.getRL(self.dc)

    def reCalc(self, one_sided = None):
        self.__init__(self.snpFile, one_sided)
        self.getParameters()


    def getWorstMargin(self, parameter):
        if parameter in self.worstMargin:
            return self.worstMargin[parameter]
        PassFail = "Pass"
        param = getattr(self, parameter)
        pairs = param.keys()
        worst = {}  
        limit = None
        if self.standard:
            if parameter in self.standard.limits:
                limit = self.standard.limits[parameter].getDict() #.evaluateDict({"f": self.freq} , len(self.freq), neg=not(parameter=="PropagationDelay"))
            for pair in pairs:
                value = ''
                freq = ''
                lim = ''
                worstMargin = ''
                if limit:
                    margins, frequencies, values = self.getMargins(param[pair], limit, parameter)
                    if len(margins) > 0:
                        worstMargin, index = self.advancedMin(margins)
                        worstMargin = abs(worstMargin)
                        value = values[index]
                        freq = frequencies[index]
                        lim = limit[freq]
                        if value > lim and not parameter == "IL":
                            PassFail = "Fail"
                        elif value < lim and parameter == "IL":
                            PassFail = "Fail"
                
                worst[pair] = (value, freq, lim, worstMargin)
            self.worstMargin[parameter] = (worst, PassFail)
        return worst, PassFail

    def getWorstValue(self, parameter):
        if parameter in self.worstValue:
            return self.worstValue[parameter]
        PassFail = "Pass"
        param = getattr(self, parameter)
        pairs = param.keys()
        worst = {}
        limit = None
        if self.standard:
            if parameter in self.standard.limits:

                limit = self.standard.limits[parameter].getDict() #.evaluateDict({"f": self.freq} , len(self.freq), neg=not(parameter=="PropagationDelay"))
            for pair in pairs:
                validMin = False
                value = np.array(param[pair])
                while not validMin:
                    worstValue, index = self.advancedMax(value)
                    freq = self.freq[index]
                    if limit:
                        if freq in limit:
                            lim = limit[freq]
                            margin = abs(worstValue - limit[freq])
                            if worstValue > lim and not parameter == "IL":
                                PassFail = "Fail"
                            elif worstValue < lim and parameter == "IL":
                                PassFail = "Fail"
                            validMin = True
                        else:
                            value = np.delete(value, index)
                    else:
                        margin = ''
                        lim = ''
                        validMin = True
                worst[pair] = (worstValue, freq, lim, margin)
            self.worstValue[parameter] = (worst, PassFail)
        return worst, PassFail


    def __repr__(self):
        return "SNP"
    

    def advancedMin(self , vals):
        return min(vals), list(vals).index(min(vals))

    def advancedMax(self , vals):
        return max(vals), list(vals).index(max(vals))

    def getMargins(self, measurements, limit, parameter):
        margins = []
        freq = []
        values = []
        i = 0
        for val in measurements:
            if self.freq[i] in limit:
                if parameter == "IL":
                    margins.append(val - limit[self.freq[i]])
                else:
                    margins.append(limit[self.freq[i]] - val)
                freq.append(self.freq[i])
                values.append(val)
            i+=1
        return margins, freq, values

    def evaluateLimit(self, param):
        print("Evaulating : ", param)
        #self.standard.limits[param].None

        self.standard.limits[param].evaluateArray({"f": self.freq} , len(self.freq), neg=not(param=="PropagationDelay"))
        self.standard.limits[param].evaluateDict({"f": self.freq} , len(self.freq), neg=not(param=="PropagationDelay"))
        #print("ERROR: Limit Not evaluated", param)
            


    def setStandard(self, standard):
        self.standard = standard
        self.worstMargin = {}
        self.worstValue = {}

       # with ProcessPool(cpu_count()) as p:
        for parameter in self.parameters:
            try:
                self.evaluateLimit(parameter.replace(" ", "") )
                

                self.getWorstMargin(parameter.replace(" ", ""))
                self.getWorstValue(parameter.replace(" ", ""))

            except Exception as e:
                print("ERROR: Limit Not evaluated", parameter)

            
        print("FINISHED SETTING STANDARD")



    def ret_function(self):
        pass
        #marginWorker.finished.connect(self.displaySamplesInTable)

    def getParam(self, paramName, z=False):
        #This functions returns the dictionairy accosiated to a parameter.
        #For example getParam("RL") --> {"12" : [...],
        #                                "36" : [...]}
        try:
            if paramName == "Propagation Delay":
                paramName = "PropagationDelay"
            if z:
                paramName += "Z"
            return getattr(self, paramName)
        except:
            return None




if __name__ == "__main__":
    
    samp = Sample(r"snps\TestPCLiam3.s8p")
    
    samp.getParameters()

    print(samp.RLZ["12"][0])


