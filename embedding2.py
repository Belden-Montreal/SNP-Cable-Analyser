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

        self.directFixtureDelay = {}
        self.plugDelay = {}
        self.plugNextDelay = {}
        self.plugJackDelay = {}
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

        self.k1 = 5e-12     #Pair Shorting jack 12, 45, 78
        self.k2 = 14e-12    #Pair Shorting jack 36
        self.k3 = 20e-12    #Thru calibration

        self.reembeded = {}


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


    def getDirectFixtureDelay(self, openSNP, shortSNP):
        '''
        This function is used to calculate the Delay of the Direct Fixture.
        It must be called before finding the delay of the plug to allow for correction of the delay on the plug
        It finds the average delay of an open measurement and a short measurement on each pair from 100MHZ to 500MHZ. 
        '''
        
        print("Calculating Direct Fixture Delay")

        self.openSample = openSNP
        self.shortSample = shortSNP
        
        openDelay = self.getOpenDelay()
        shortDelay = self.getShortDelay()

        #print("DF Open Delay = ", openDelay["12"][0])
        
        #directFixtureDelay = {} #initialize the DF dictionairy.

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        self.freq = self.openSample.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(self.freq)
        for pair in pairs:
            #first Find 100MHz and 500MHz
            f100 = list(self.openSample.freq.astype(int)).index(100)
            f500 = list(self.openSample.freq.astype(int)).index(500)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500])
            self.directFixtureDelay[pair] = (openAvg + shortAvg)/4


        return self.directFixtureDelay
    

    def getPlugDelay(self, openSNP, shortSNP):

        '''
        Once the direct fixture delay has been calculated, the plug delay can be calculated.
        Like getDirectFixtureDelay(), this fucntion returns the delay of an open measurement
        and a short measurement on each pair from 100MHZ to 500MHZ. 
        '''

        self.openSample = openSNP
        self.shortSample = shortSNP
        
        openDelay = self.getOpenDelay()
        shortDelay = self.getShortDelay()

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        freq = self.openSample.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(freq)

               
        for pair in pairs:
            f100 = list(self.openSample.freq.astype(int)).index(100)
            f500 = list(self.openSample.freq.astype(int)).index(500)
            #print("f100 ", f100)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500]) 

            self.plugDelay[pair] = ((openAvg + shortAvg - self.k1 - self.k2) / 4) - self.directFixtureDelay[pair] + self.k3

        print("Plug Delay ", self.plugDelay)
        return self.plugDelay


    def getPlugNextDelay(self):
        '''
        This function calculates the Next Delay of the plug
        '''
        print("plugDelay Keys: ", self.plugDelay.keys())

        self.plugNextDelay["12-36"] = self.plugDelay["12"] + self.plugDelay["36"]
        self.plugNextDelay["45-12"] = self.plugDelay["12"] + self.plugDelay["45"]
        self.plugNextDelay["12-78"] = self.plugDelay["12"] + self.plugDelay["78"]
        self.plugNextDelay["45-36"] = self.plugDelay["36"] + self.plugDelay["45"]
        self.plugNextDelay["36-78"] = self.plugDelay["36"] + self.plugDelay["78"]
        self.plugNextDelay["45-78"] = self.plugDelay["45"] + self.plugDelay["78"]

        return self.plugNextDelay


    def correctPlugVector(self, loadSNP):

        '''
        This function calculates the new vector for the plug, based on its  delay that was found in getPlugDelay() and  getPlugNextDelay()
        '''
        
        self.loadSample = loadSNP

        plugNextNoCorrection = self.loadSample.getNEXT(self.loadSample.dd, z=True)

        self.minFreq = self.loadSample.freq[0]
        self.maxFreq = self.loadSample.freq[-1]
        self.numPoints = len(self.loadSample.freq)
        
        print("Plug No corr ",plugNextNoCorrection.keys())
        self.correctedPlugVector = {}
        for key in plugNextNoCorrection.keys():
            
            self.correctedPlugVector[key] = []
            
            for f in range(0, len(plugNextNoCorrection[key])):
                #To correct the phase, we must first calculate the old phase
                phase_calib = np.angle(plugNextNoCorrection[key][f], deg=True)
                #Using the old phase and the delay, we will calculate the corrected phase
                phase_corrected = phase_calib + 360 * self.loadSample.freq[f] * self.plugNextDelay[key]

                if(key == "45-36" and self.loadSample.freq[f] == 100):
                    print("freq: ", self.loadSample.freq[f])
                    print("Next No corr : ", plugNextNoCorrection[key][f])
                    print("Correct Plug Phase :", phase_corrected)
                    print("Old Plug Phase :", phase_calib)
    
                #Then we'll calculate the amplitude
                amplitude = np.abs(plugNextNoCorrection[key][f])

                #By keeping the amplitude the same, we can use the corrected phase to find the new Real and Immaginary components.
                real = amplitude * np.cos(phase_corrected * np.pi/180)
                imag = amplitude * np.sin(phase_corrected * np.pi/180)
                
                #And finally we add the new next with the corrected phase to the corrected plug dictionary
                self.correctedPlugVector[key].append(complex(real, imag))

                if(key == "45-36" and self.loadSample.freq[f] == 100):
                    print("Correct Plug Vect = "+  str(self.correctedPlugVector[key][f]) + "@ pair :" + key)
                    print("Correct Vect: ", complex(real, imag))         
        
        return self.correctedPlugVector


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
        print()
        #testPlugFile = open(self.jackName, "w")
        #testPlugFile.write(json.dumps(self.jackVector))
        #testPlugFile.close
           
        return self.jackNextDelay
    

    def setPlugVectors(self, cat):

        if cat == "6A" or cat == "6":
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
            self.case1  = lambda f: (-35.8- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case2  = lambda f:([], [])
            self.case3  = lambda f:([], [])
            self.case4  = lambda f: (-39.5- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["45-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case5  = lambda f: (-42.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case6  = lambda f: (-50.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True))
            self.case7  = lambda f: (-42.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["12-36"][list(self.loadSample.freq).index(f)], deg=True)) 
            self.case8  = lambda f: (-50.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["36-78"][list(self.loadSample.freq).index(f)], deg=True))
            self.case9  = lambda f: (-50.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["45-12"][list(self.loadSample.freq).index(f)], deg=True))
            self.case10 = lambda f:([],[])
            self.case11 = lambda f: (-50.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["45-78"][list(self.loadSample.freq).index(f)], deg=True))
            self.case12 = lambda f:([], [])
            self.case13 = lambda f: (-60.0- 20 * np.log10((f)/100), np.angle(self.correctedPlugVector["12-78"][list(self.loadSample.freq).index(f)], deg=True))
            self.case14 = lambda f:([], [])

    def reembed(self):

        self.setPlugVectors("6A")
        self.reembeded = {}
        self.freq = self.loadSample.freq 

        for i in range(1,15):
            #First, we will declare the reembeded array
            self.reembeded[i] = []
            
            mag_phase = getattr(self, "case" + str(i))
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


    def addPlug(self, dfOpen, dfShort, pdfOpen, pdfShort, pdfLoad, plugName = None ):
        '''
        This function is used to calculate the plug and export its data into a file
        df  -> Direct Fixture
        pdf -> Plug and Direct Fixture
        '''


        
        
        directFixtureDelay = self.getDirectFixtureDelay(dfOpen, dfShort) #Dictionairy of the delay in seconds on each pair

        plugDelay = self.getPlugDelay(pdfOpen, pdfShort) #Dictionairy of the delay in seconds on each pair
        plugNextDelay = self.getPlugNextDelay() #Dictionairy of the delay in seconds on each pair combination ex.: {12-36, 12-45}
        print("plugDirectFixtureLoad, " , pdfLoad)
        correctedPlugVector = self.correctPlugVector(pdfLoad) #Dictionairy of arrays of the corrected vector for the plug ex,: {12-36 : [...]}

        #Now we'll write to the xml file the plugs data as elements 
        if plugName:

            if not os.path.isdir(self.plugFolder):
                os.mkdir(self.plugFolder)
            file = self.plugFolder + plugName + ".xml"
            
            plug      = ET.Element("plug")
            plug.set('name', plugName)  

            minFreq   = ET.SubElement(plug, "minFreq")
            minFreq.text = str(self.minFreq)
            
            maxFreq   = ET.SubElement(plug, "maxFreq")
            maxFreq.text = str(self.maxFreq)
            
            numPoints = ET.SubElement(plug, "numPoints")
            numPoints.text = str(self.numPoints)

            plugDelayElement = ET.SubElement(plug, "plugDelay")

            for key in plugDelay.keys():
                pair = ET.SubElement(plugDelayElement, "pair_"+ key)
                print(key)
                pair.text = str(plugDelay[key])

            plugNextDelayElement = ET.SubElement(plug, "plugNextDelay")
         
            for key in plugNextDelay.keys():
                pair = ET.SubElement(plugNextDelayElement, "Next_"+ key)
                pair.text = str(plugNextDelay[key])

            correctedPlugVectorElement = ET.SubElement(plug, "correctedPlugVector")
            for key in correctedPlugVector.keys():
                pair = ET.SubElement(correctedPlugVectorElement, "Next_"+key)
                pair.text = str(correctedPlugVector[key])

            if os.path.isfile(file):
                raise Exception('File Already Exists')
                return

            mydata = ET.tostring(plug)
            myfile = open(file, "wb")  
            myfile.write(mydata)

        return correctedPlugVector


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
        
        params = {""
                  "36-45": ["case1", "case2", "case3", "case4"],
                  "12-36": ["case5", "case6"],
                  "36-78": ["case7", "case8"],
                  "12-45": ["case9", "case10"],
                  "45-78": ["case11", "case12"],
                  "12-78": ["case13", "case14"]}

        return params
            

    def __retr__(self):
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
    

    
