from snpAnalyze import SNPManipulations
import numpy as np
import os
import json

import xlsxwriter
import sympy

import matplotlib.pyplot as plt

import time

import xml.etree.ElementTree as ET
import xmltodict

import os

class Embedding(SNPManipulations):

    def __init__(self, testName = "DEEMBED_1"):


        self.embeddedOpen = " "
        self.embeddedShort = " "
        self.embeddedLoad = " "


        self.jackDelay = {}
        self.jackNextDelay = {}

        self.correctedPlugVector = {}
        self.name = testName  # "DEEMBED_1"
        self.date = time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
        self.limit = None
        
        self.plugName = "TestPlug"
        self.jackName = "TestJack"

        self.plugFolder = "plugs/"

        #self.workbook = xlsxwriter.Workbook(self.testName + ".xlsx")

        # TIA-568.2-D-2018.pdf  --> p.216 --> (C.6.5.11.3.2)  --> #6
        #Delay_round_trip_plug_jack
        self.k1 = 5e-12     #Pair Shorting jack 12, 45, 78
        self.k2 = 14e-12    #Pair Shorting jack 36
        self.k3 = 20e-12    #Thru calibration

        self.reembeded = {}
        self.cat = "6A"

        self.standard = None

    def getOpenDelay(self):
        '''
        Using aquired S8P for an open sample, this function returns the progation delay
        on all pairs
        '''
        print("Num Samples = ", self.openSample.num_samples)
        return self.openSample.getPropagationDelay()
    
    def getShortDelay(self):
        '''
        Using aquired S8P for a shorted sample, this function returns the progation delay
        on all pairs
        '''
        return self.shortSample.getPropagationDelay()



    

 





    def getJackVector(self, loadSNP):
        
        '''
        This function takes in the SNP of the mated maesurment (Jack + Test Plug)
        and extracts the Jack Vector
        '''
        
        self.loadSample = loadSNP       #Mated sample

        self.matedNextNoCorrection = self.loadSample.getNEXT(self.loadSample.dd, z=True)

        self.jackVector = {}

        for key in self.matedNextNoCorrection.keys():
            self.jackVector[key] = []
            for f in range(0, len(self.matedNextNoCorrection[key])):
                #To correct the phase, we must first calculate the old phase
                phase_calib = np.angle(self.matedNextNoCorrection[key][f], deg=True)
                #Using the old phase and the delay, we will calculate the corrected phase
                phase_corrected = phase_calib + 360 * self.loadSample.freq[f] * self.plugNextDelay[key]
                #Then we'll calculate the amplitude
                amplitude = np.abs(self.matedNextNoCorrection[key][f])

                #By keeping the amplitude the same, we can use the corrected phase to find the new Real and Immaginary components.
                real = amplitude * np.cos(phase_corrected * np.pi/180)
                imag = amplitude * np.sin(phase_corrected * np.pi/180)
                matedNextCorrected = complex(real, imag)
                self.jackVector[key].append(matedNextCorrected - self.correctedPlugVector[key][f])
                
        #And then we write the corrected jack Next dictionary to a json file
        print(self.jackVector["12-36"][2])
        print()
        #testPlugFile = open(self.jackName, "w")
        #testPlugFile.write(json.dumps(self.jackVector))
        #testPlugFile.close
      
        return self.jackVector


    def getJackVectorReverse(self, openSNP, shortSNP, loadSNP):

        self.openSample = openSNP
        self.shortSample = shortSNP
        self.loadSample = loadSNP

        openDelay = self.getOpenDelay()
        shortDelay = self.getShortDelay()

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        freq = self.openSample.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(freq)
        self.matedNextNoCorrection = {}
        for pair in pairs:
            f100 = list(self.openSample.freq.astype(int)).index(100)
            f500 = list(self.openSample.freq.astype(int)).index(500)
            print("f100 ", f100)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500]) 
            print(self.correctedPlugVector.keys())
            #correctedPlug = np.mean(self.correctedPlugVector[pair][f100:f500])

            print(self.k3)
            self.jackDelay[pair] = ((openAvg + shortAvg - float(self.k1) - float(self.k2) )/4)  - self.plugDelay[pair] + float(self.k3)
            
            
        self.jackNextDelay["12-36"] = self.jackDelay["12"] + self.jackDelay["36"]
        self.jackNextDelay["45-12"] = self.jackDelay["12"] + self.jackDelay["45"]
        self.jackNextDelay["12-78"] = self.jackDelay["12"] + self.jackDelay["78"]
        self.jackNextDelay["45-36"] = self.jackDelay["36"] + self.jackDelay["45"]
        self.jackNextDelay["36-78"] = self.jackDelay["36"] + self.jackDelay["78"]
        self.jackNextDelay["45-78"] = self.jackDelay["45"] + self.jackDelay["78"]

        self.matedNextNoCorrection = self.loadSample.getNEXT(self.loadSample.dd, z=True)
        
        self.jackVector = {}
        
        for key in self.matedNextNoCorrection.keys():
            self.jackVector[key] = []
            for f in range(0, len(self.matedNextNoCorrection[key])):
                #To correct the phase, we must first calculate the old phase
                phase_calib = np.angle(self.matedNextNoCorrection[key][f], deg=True)
                #Using the old phase and the delay, we will calculate the corrected phase
                phase_corrected = phase_calib + 360 * self.loadSample.freq[f] * self.jackNextDelay[key]
                #Then we'll calculate the amplitude
                amplitude = np.abs(self.matedNextNoCorrection[key][f])

                #By keeping the amplitude the same, we can use the corrected phase to find the new Real and Immaginary components.
                real = amplitude * np.cos(phase_corrected * np.pi/180)
                imag = amplitude * np.sin(phase_corrected * np.pi/180)
                matedNextCorrected = complex(real, imag)
                self.jackVector[key].append(matedNextCorrected - self.correctedPlugVector[key][f])
                
        #And then we write the corrected jack Next dictionary to a json file
        print(self.jackVector["12-36"][2])
        #testPlugFile = open(self.jackName, "w")
        #testPlugFile.write(json.dumps(self.jackVector))
        #testPlugFile.close
           
        return self.jackNextDelay
    

    def setPlugVectors(self, cat):
        self.cat = cat
        if cat == "6A" or cat == "6" or cat == "8":
            self.case1  = lambda f: (-(38.1-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case2  = lambda f: (-(38.6-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case3  = lambda f: (-(39.0 -20*np.log10((f)/100)), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case4  = lambda f: (-(39.5-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case5  = lambda f: (-(46.5-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case6  = lambda f: (-(49.5-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case7  = lambda f: (-(46.5-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["36-78"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case8  = lambda f: (-(49.5-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["36-78"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case9  = lambda f: (-(57.0-20*np.log10((f)/100)), 90) 
            self.case10 = lambda f: (-(70.0-20*np.log10((f)/100)), -90)  
            self.case11 = lambda f: (-(57.0-20*np.log10((f)/100)), 90) 
            self.case12 = lambda f: (-(70.0-20*np.log10((f)/100)), -90) 
            self.case13 = lambda f: (-(66.0-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["12-78"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case14 = lambda f: (-(66.0-20*np.log10((f)/100)), np.angle(self.correctedPlugVector["12-78"][list(self.loadSample.freq).index(f)], deg=True)-180)

        elif cat == "5":
            self.case1  = lambda f: (-(35.8- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case2  = lambda f:(None, None)
            self.case3  = lambda f:(None, None)
            self.case4  = lambda f: (-(39.5- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case5  = lambda f: (-(42.0- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case6  = lambda f: (-(50.0- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case7  = lambda f: (-(42.0- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case8  = lambda f: (-(50.0- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["36-78"][list(self.loadSample.freq).index(f)], deg=True))
            self.case9  = lambda f: (-(50.0- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["45-12"][list(self.loadSample.freq).index(f)], deg=True))
            self.case10 = lambda f:(None, None)
            self.case11 = lambda f: (-50.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["45-78"][list(self.loadSample.freq).index(f)], deg=True))
            self.case12 = lambda f:(None, None)
            self.case13 = lambda f: (-(60.0- 20 * np.log10((f)/100)), np.angle(self.correctedPlugVector["12-78"][list(self.loadSample.freq).index(f)], deg=True))
            self.case14 = lambda f:(None, None)

    def reembed(self, case = "6A"):

        self.setPlugVectors(case)
        self.reembeded = {}
        self.freq = self.loadSample.freq 

        for i in range(1,15):
            #First, we make sure the case is not N/A
            mag_phase = getattr(self, "case" + str(i))
            if mag_phase(1)[0] is None:
                continue

            #Then, we  declare the reembeded array
            self.reembeded[i] = []

            for j, f in enumerate(self.loadSample.freq):
                #Get the coresponding case magnetide and convert it to Complex
               
                plug_f = mag_phase(f)

                #print("pluf_f = " , plug_f)

                amplitude = 10**(plug_f[0]/20)
                phase = plug_f[1]
                #print("phase = " , phase)
                real = amplitude * np.cos(phase * np.pi/180)
                imag = amplitude * np.sin(phase * np.pi/180)
                plugRI = complex(real, imag)
                key = ["45-36", "45-36", "45-36", "45-36", "12-36", "12-36", "36-78", "36-78", "45-12", "45-12", "45-78", "45-78", "12-78", "12-78"][i-1]
                reembed = plugRI + self.jackVector[key][j]
                self.reembeded[i].append(20*np.log10(reembed))
        print(list(self.loadSample.freq))     

        f10 = list(self.loadSample.freq.astype(int)).index(10)
        f100 = list(self.loadSample.freq.astype(int)).index(100)

        f500 = list(self.loadSample.freq.astype(int)).index(500)



    def getPlugList(self):
        '''
        This function lists all the plugs in the plugs directory
        '''
        listOfFiles = os.listdir(self.plugFolder)
        listOfPlugs = []
        for file in listOfFiles:
            listOfPlugs.append(file.replace('.xml', ''))
        return listOfPlugs

    def getPlugParams(self,  plugXML):
        '''
        This function extracts the parameters of a given plug from its XML file
        '''
        with open(self.plugFolder + plugXML) as fd:
            plug = xmltodict.parse(fd.read())

        self.plugDelay = {} 
        for key in plug['plug']['plugDelay'].keys():
            pair = key.replace('pair_', '')
            self.plugDelay[pair] = float(plug['plug']['plugDelay'][key])

        self.plugNextDelay = {} 
        for key in plug['plug']['plugNextDelay'].keys():
            pair = key.replace('Next_', '')
            self.plugNextDelay[pair] = float(plug['plug']['plugNextDelay'][key])

        self.correctedPlugVector = {} 
        for key in plug['plug']['correctedPlugVector'].keys():
            pair = key.replace('Next_', '')
            self.correctedPlugVector[pair] = eval(plug['plug']['correctedPlugVector'][key])


    def getParameters(self):
        
        if self.cat == "5":
            params = {""
                    "36-45": ["case1", "case4"],
                    "12-36": ["case5", "case6"],
                    "36-78": ["case7", "case8"],
                    "12-45": ["case9"],
                    "45-78": ["case11"],
                    "12-78": ["case13"]}

        if self.cat == "6" or self.cat == "6A" or self.cat == "8":    
            params = {""
                    "36-45": ["case1", "case2", "case3", "case4"],
                    "12-36": ["case5", "case6"],
                    "36-78": ["case7", "case8"],
                    "12-45": ["case9", "case10"],
                    "45-78": ["case11", "case12"],
                    "12-78": ["case13", "case14"]}

        return params
            

    def __repr__(self):
        return "Embed"
        
    @property
    def openSample(self):
        return self._openSample

    @openSample.setter
    def openSample(self, openSNP):
        self._openSample = SNPManipulations(openSNP)       
        self._openSample.s2mm()
        self._openSample.port_name = {0:"45", 1:"12", 2:"36", 3:"78"}
        self._openSample.one_sided = True


    @property
    def shortSample(self):
        return self._shortSample

    @shortSample.setter
    def shortSample(self, shortSNP):
        self._shortSample = SNPManipulations(shortSNP)
        self._shortSample.s2mm()
        self._shortSample.port_name = {0:"45", 1:"12", 2:"36", 3:"78"}
        self._shortSample.one_sided = True
    @property
    def loadSample(self):
        return self._loadSample
    
    @loadSample.setter
    def loadSample(self, loadSNP):
        self._loadSample = SNPManipulations(loadSNP)
        self._loadSample.s2mm()
        self._loadSample.port_name = {0:"45", 1:"12", 2:"36", 3:"78"}
        self._loadSample.one_sided = True

if __name__ == "__main__":

    print("Start")
    em = Embedding()
    
    directFixtureShort = "snps\DEEMBED TEST\DirectFixShort.s8p"
    directFixtureOpen  = "snps\DEEMBED TEST\DirectFixOpen.s8p"

    plugDirectFixtureShort = "snps\DEEMBED TEST\DirectFixPlugShort.s8p"
    plugDirectFixtureOpen = "snps\DEEMBED TEST\DirectFixPlugOpen.s8p"
    plugDirectFixtureLoad = "snps\DEEMBED TEST\DirectFixPlugLoad2.s8p"

    plugJackLoad = "snps\DEEMBED TEST\MatingPlugJackForward.s8p"

    jackPlugReverse = "snps\DEEMBED TEST\MatingPlugJacktReverse.s8p"
    jackPlugOpen = "snps\DEEMBED TEST\MatingPlugJackOpen.s8p"
    jackPlugShort = "snps\DEEMBED TEST\MatingPlugJackShort.s8p"

    '''em.getDirectFixtureDelay(directFixtureOpen, directFixtureShort)
    em.getPlugDelay(plugDirectFixtureOpen, plugDirectFixtureShort)
    em.getPlugNextDelay()
    em.correctPlugVector(plugDirectFixtureLoad)'''

    em.addPlug(directFixtureOpen, directFixtureShort, plugDirectFixtureOpen, plugDirectFixtureShort, plugDirectFixtureLoad)
    print(em.getPlugList())
    em.getPlugParams('PlugTest.xml')

    
    #em.getJackVector(plugJackLoad)
    em.getJackVectorReverse(jackPlugOpen, jackPlugShort, jackPlugReverse)
    
    em.reembed()
    

    
