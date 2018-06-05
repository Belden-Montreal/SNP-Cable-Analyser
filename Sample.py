from snpAnalyze import SNPManipulations
import os
from os.path import splitext
import time
import numpy as np

class Sample(SNPManipulations):

    '''This class handles the SNP samples for the basic test'''

    def __init__(self, snpFile, one_sided = None):


        self.snpFile = snpFile

        self.rs = super(Sample, self)
        self.rs.__init__(self.snpFile)
        #self.renumber(renumFrom, renumTo)
        self.s2mm()
        self.port_name = {0:"12", 1:"36", 2:"45", 3:"78"}

        self.name, self.extension = splitext(os.path.basename(snpFile))
        self.date = time.ctime(os.path.getctime(snpFile))
        #print self.date

        self.standard = None

        if one_sided != None:
            self.one_sided = one_sided
        
        elif self.getNumPorts(self.dd) == 4: #Assume that the test is one-sided.
                                             #This can be changed
            self.one_sided = True

        elif self.getNumPorts(self.dd) == 8: #Assume that test is end to end.
            self.one_sided = False

        self.port_name = {}
        self.pair_combo = ["45", "12","36","78"]
        
        if self.one_sided:
            for i in range(0, self.getNumPorts(self.dd)):
                self.port_name[i] = self.pair_combo[i]  #{0:"12", 1:"36", 2:"45", 3:"78"}
            self.parameters = ["RL", "NEXT", "Propagation Delay", "PSNEXT", "LCL", "TCL", "CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]
        else:
            for i in range(0, self.getNumPorts(self.dd)//2):
                self.port_name[i] = self.pair_combo[i]  #{0:"12", 1:"36", 2:"45", 3:"78"}
            for i in range((self.getNumPorts(self.dd)//2), self.getNumPorts(self.dd)):
                self.port_name[i] = "(r)"+self.pair_combo[i-self.getNumPorts(self.dd)//2]  #{4:"(r)12",  :"(r)36", 6:"(r)45", 7:"(r)78", 0:"12", 1:"36", 2:"45", 3:"78"}
            self.parameters = ["RL", "IL", "NEXT", "Propagation Delay", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]

            

        #print self.port_name
        
        
        #vna_out.write_touchstone("testout_mm", form="ri")
    
        #print self.RL["RL_11"][0]

    '''@limit.setter
    def setLimit(self, ):
        self.limit = Limit()'''
        

    def getParameters(self, z=False):

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
        PassFail = "Pass"
        param = getattr(self, parameter)
        pairs = param.keys()
        worst = {}
        limit = None
        if self.standard:
            if parameter in self.standard.limits:
                limit = self.standard.limits[parameter].evaluateDict({"f": self.freq} , len(self.freq), neg=True)
            for pair in pairs:
                value = ''
                freq = ''
                lim = ''
                worstMargin = ''
                if limit:
                    margins, frequencies, values = self.getMargins(param[pair], limit)
                    if len(margins) > 0:
                        worstMargin, index = self.advancedMin(margins)
                        worstMargin = abs(worstMargin)
                        value = values[index]
                        freq = frequencies[index]
                        lim = limit[freq]
                        if value > lim:
                            PassFail = "Fail"
                
                worst[pair] = (value, freq, lim, worstMargin)
    
        return worst, PassFail

    def getWorstValue(self, parameter):

        PassFail = "Pass"
        
        param = getattr(self, parameter)
        pairs = param.keys()
        worst = {}
        limit = None
        if self.standard:
            if parameter in self.standard.limits:
                limit = self.standard.limits[parameter].evaluateDict({"f": self.freq} , len(self.freq), neg=True)
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
                            if  worstValue > lim:
                                PassFail = "Fail"
                            validMin = True
                        else:
                            value = np.delete(value, index)
                    else:
                        margin = ''
                        lim = ''
                        validMin = True
                worst[pair] = (worstValue, freq, lim, margin)

    

        return worst, PassFail


    def __retr__(self):
        return "SNP"
    

    def advancedMin(self , vals):
        return min(vals), list(vals).index(min(vals))

    def advancedMax(self , vals):
        return max(vals), list(vals).index(max(vals))

    def getMargins(self, measurements, limit):
        margins = []
        freq = []
        values = []
        i = 0
        for val in measurements:
            if self.freq[i] in limit:
                margins.append(limit[self.freq[i]] - val)
                freq.append(self.freq[i])
                values.append(val)
            i+=1
        return margins, freq, values

if __name__ == "__main__":
    
    samp = Sample('fci.s4p')
    
    samp.extractParameters(samp.dd)

    #print samp.RL["RL_11"][0]

