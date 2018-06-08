from snpAnalyze import SNPManipulations
import os
from os.path import splitext
import time


import numpy as np

import re 
class Alien(object):

    def __init__(self, testName):

        self.name = testName
        self.date = time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
        self.limit = None
        
        self.numPairs = 8
        self.pair_combo = []
        #for i in self.numPairs:
            #self.PSANEXT[]

        self.powerSum = {}
        self.averagePowerSum = {}

        #self.port_name = {0:"12", 1:"36", 2:"45", 3:"78",4:"12", 5:"36", 6:"45", 7:"78"}

        self.port_name = {}
        self.pair_combo = ["45", "12","36","78"]
        
  
        for i in range(0, self.numPairs//2):
            self.port_name[i] = self.pair_combo[i]  #{0:"12", 1:"36", 2:"45", 3:"78"}
            print("loop 1", i)
        for i in range(self.numPairs//2, self.numPairs):
            self.port_name[i] =  "(d)"+self.pair_combo[i-self.numPairs]  #{4:"(r)12",  :"(r)36", 6:"(r)45", 7:"(r)78", 0:"12", 1:"36", 2:"45", 3:"78"}
            print("loop 2", i)

        print(self.port_name)

        self.disturbersList = []

        self.disturbers = {}
        self.disturbers["end1"] = {}
        self.disturbers["end2"] = {}

        self.disturbers["end1"]["ANEXT"]   = {}
        self.disturbers["end1"]["AFEXT"]   = {}
        self.disturbers["end1"]["PSANEXT"] = {}
        self.disturbers["end1"]["PSAFEXT"] = {}
        self.disturbers["end1"]["PSAACRF"] = {}
        
        self.disturbers["end2"]["ANEXT"]   = {}
        self.disturbers["end2"]["AFEXT"]   = {}
        self.disturbers["end2"]["PSANEXT"] = {}
        self.disturbers["end2"]["PSAFEXT"] = {}
        self.disturbers["end2"]["PSAACRF"] = {}
            

    def addDisturbed(self, snpFile):
        self.rs = SNPManipulations(snpFile)
        self.rs.oneSided = False
    
        #vna_out.renumber([1,2], [2,1])

        self.rs.s2mm()

        self.rs.port_name = self.port_name
        
        self.distrubedIL = self.rs.getIL(self.rs.dd , z = False)
        
    def addDisturberMeasurement(self, end, testType, snpFile, name = ""):

        '''
        This function accepts as parameters the following:
            -end : the end of the cable 
            -measurement: the type of measurement requested to taken on said cable (ANEXT, AFEXT).
            -name: This is the name of the dsturbing cable.
                   If the name arleady exists, then the disturbers measurements will be overwritten, or a measurement will be added to it.
            Once a measured value has been added, this function will procede to call the desired functions (getANEXT, getPSANEXT, getAveragePSANEXT).    
        '''

        alien = self.getAlien(snpFile)   #Wether its ANEXT or AFEXT, the method to extract from the SNP is the same. 

        self.disturbers[end][testType][name] = alien

        print(self.disturbers[end][testType][name].keys())
 

    def getAlien(self, snpFile):
        '''
        To get the ANEXT, we will get the FEXT and the IL from the snp file and we'll combine the 2 dicts.
        '''
        
        self.rs = SNPManipulations(snpFile)
        self.rs.oneSided = False
    
        #vna_out.renumber([1,2], [2,1])
        
        self.rs.s2mm()
        self.freq = self.rs.freq

        self.rs.port_name = self.port_name
        
        FEXT = self.rs.getFEXT(self.rs.dd, z=False)
        PSFEXT = self.rs.getPSFEXT(self.rs.dd)
        IL = self.rs.getIL(self.rs.dd, z=False)

        print(FEXT.keys())
       
        #we must modify the IL dictionnary keys from 12 - > 12-12

        ILKeys = list(IL.keys())

        print ("IL Keys : ", ILKeys)

        for key in ILKeys:
            IL[re.sub('[(d)]', '', key) + "-(d)" + key] = IL[key]
            del IL[key]
        print ("IL Keys : ", IL.keys())

        #print({**FEXT, **IL}.keys())

        #return FEXT
        return {**FEXT, **IL}
    

    def getPSAlien(self, end, Test, disturbers):
        
        #print (self.disturbers["dist_1"][end]["ANEXT"].keys())
        numDisturbers = len(self.disturbers.keys())
        numPairs = self.numPairs

        #activeDisturbers = self.disturbers
        #disturbers = activeDisturbers.keys()
        self.PSAlien = {}

        self.disturbersList = disturbers
        
        for disturbed_pair in range( numPairs //2):
            self.PSAlien[self.port_name[disturbed_pair]] = []

            for f in range(0, self.rs.num_samples):
                outterSum = 0
                for disturber in disturbers:

                    innerSum = 0
                    for disturbing_pair in range(numPairs//2, numPairs):
                        ALIEN = self.disturbers[end][Test][disturber][self.port_name[disturbed_pair] + '-' + self.port_name[disturbing_pair]][f]

                        if f == 0:
                            print(str(disturbed_pair) + '-' + str(disturbing_pair), ALIEN)
                        #inner = 10**(ANEXT_k_i_j/10)
                        
                        '''if f == 0 and  disturbed_pair == numPairs - 1:
                            #print(disturbing_pair)
                            print(disturber, disturbed_pair, innerSum, self.port_name[disturbed_pair] + '-' + self.port_name[disturbing_pair], ANEXT)
                            #print (disturbing_pair)'''

                        innerSum += 10**(ALIEN/10)
                    outterSum += innerSum
                    if f == 0 and disturbed_pair == 0:
                        print("inner", innerSum)
                PSK = 10*np.log10(outterSum)
                self.PSAlien[self.port_name[disturbed_pair]].append(PSK)
                
        return self.PSAlien
                
    def getPSAACRX(self, end, Test):

        '''Gets either PSAACRF or PSAACRN'''
        
        numDisturbers = len(self.disturbers.keys())
        numPairs = self.numPairs

        activeDisturbers = self.disturbers
        disturbers = activeDisturbers.keys()

        PSAACRX = {}
        
        for disturbed_pair in range(numPairs // 2):
            PSAACRX[self.port_name[disturbed_pair]] = []
            for f in range(0, self.rs.num_samples):
                PS = self.PSAlien
                PSAACRX[self.port_name[disturbed_pair]].append(PS[self.port_name[disturbed_pair]][f] - self.distrubedIL[self.port_name[disturbed_pair]][f]) 
                if f == 0:
                    print("disturbed pair: ", self.port_name[disturbed_pair], self.distrubedIL[self.port_name[disturbed_pair]][f])

        return PSAACRX

    def __retr__(self):
        return "Alien"
        



if __name__ == "__main__":

    dist_1 = "snps/ALIEN TEST/AlienEnd1_2redo3.s16p"
    vic_IL = "snps/ALIEN TEST/Test_ALIEN_VICTIM_REDO_GOOD.s16p"
    a = Alien("Test")
    a.addDisturber("dist_1")
    a.addDisturberMeasurement("end1", "ANEXT", dist_1, "dist_1")
    a.addDisturbed(vic_IL)

    PSANEXT = a.getPSAlien("end1", "ANEXT")
    PSAACRN = a.getPSAACRX("end1", "PSANEXT")
                                                           
    print(PSAACRN.keys())
    print(PSAACRN["12"][0])      
    print(PSAACRN["36"][0])      
    print(PSAACRN["45"][0])      
    print(PSAACRN["78"][0])

    print(a.__retr__())
