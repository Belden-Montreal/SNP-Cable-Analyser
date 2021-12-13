#from reportPackages.reportlab.platypus.paragraph import P
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
from PyQt5 import QtCore     

class Plug(SNPManipulations):
    
    def __init__(self, testName = "Plug_1"):
        self.plugDelay = {}
        self.plugNextDelay = {}
        self.plugJackDelay = {}

        self.name = testName  # "DEEMBED_1"
        self.date = time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
        self.limit = None
        self.standard = None

        # TIA-568.2-D-2018.pdf  --> p.216 --> (C.6.5.11.3.2)  --> #6
        #Delay_round_trip_plug_jack
        self.k1 = 5e-12     #Pair Shorting jack 12, 45, 78
        self.k2 = 14e-12    #Pair Shorting jack 36
        self.k3 = 20e-12    #Thru calibration

        self.directFixtureDelay = {}

        self.correctedPlugVectorPhase = {}
        self.correctedPlugVectorMag = {}
        self.correctedPlugVector = {}

        self.worstValue = {}
        self.worstMargin = {}
        
        self.parameters = ["TPMag 45-36 L", "TPMag 45-36 H", "TPMag 12-36 L", "TPMag 12-36 H", "TPMag 36-78 L", "TPMag 36-78 H", "TPMag 36-78 L", "TPMag 36-78 L", "TPMag 45-12 L", "TPMag 45-12 H", "TPMag 45-78 L", "TPMag 45-78 H", "TPMag 12-78 L", "TPMag 12-78 H", "TPPhase 45-36 L", "TPPhase 45-36 H", "TPPhase 12-36 L", "TPPhase 12-36 H", "TPPhase 36-78 L", "TPPhase 36-78 H", "TPPhase 36-78 L", "TPPhase 36-78 L", "TPPhase 45-12 L", "TPPhase 45-12 H", "TPPhase 45-78 L", "TPPhase 45-78 H", "TPPhase 12-78 L", "TPPhase 12-78 H"]
        # self.getParameters()
    limitmutex = QtCore.QMutex()
    parammutex = QtCore.QMutex()
    
    def addPlug(self, dfOpen_file, dfShort_file, pdfOpen_file, pdfShort_file, pdfLoad_file, plugName = None ):
        '''
        This function is used to calculate the plug and export its data into a file
        df  -> Direct Fixture
        pdf -> Plug and Direct Fixture
        '''


        dfOpen = self.getSample(dfOpen_file)
        dfShort = self.getSample(dfShort_file)
        pdfOpen = self.getSample(pdfOpen_file)
        pdfShort = self.getSample(pdfShort_file)
        pdfLoad = self.getSample(pdfLoad_file)

        directFixtureDelay = self.getDirectFixtureDelay(dfOpen, dfShort) #Dictionairy of the delay in seconds on each pair

        plugDelay = self.getPlugDelay(pdfOpen, pdfShort) #Dictionairy of the delay in seconds on each pair
        plugNextDelay = self.getPlugNextDelay() #Dictionairy of the delay in seconds on each pair combination ex.: {12-36, 12-45}
        #print("plugDirectFixtureLoad, " , pdfLoad)
        correctedPlugVector = self.correctPlugVector(pdfLoad) #Dictionairy of arrays of the corrected vector for the plug ex,: {12-36 : [...]}
        

        self.correctedPlugVectorPhase = {}    
        self.correctedPlugVectorMag = {}    
        for pair in correctedPlugVector.keys():
            self.correctedPlugVectorMag[pair]   = 20*np.log10(np.abs(correctedPlugVector[pair]))
            self.correctedPlugVectorPhase[pair] = np.angle(correctedPlugVector[pair], deg = True)        
        


        #Now we'll write to the xml file the plugs data as elements 
        '''if plugName:

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
            myfile.write(mydata)'''
        return correctedPlugVector

    def getPlugDelay(self, pdfOpen, pdfShort):

        '''
        Once the direct fixture delay has been calculated, the plug delay can be calculated.
        Like getDirectFixtureDelay(), this fucntion returns the delay of an open measurement
        and a short measurement on each pair from 100MHZ to 500MHZ. 
        '''

        openDelay = self.getDelay(pdfOpen)
        shortDelay = self.getDelay(pdfShort)

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        freq = pdfOpen.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(freq)

               
        for pair in pairs:
            f100 = list(pdfOpen.freq.astype(int)).index(100)
            f500 = list(pdfOpen.freq.astype(int)).index(500)
            #print("f100 ", f100)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500]) 

            self.plugDelay[pair] = ((openAvg + shortAvg - self.k1 - self.k2) / 4) - self.directFixtureDelay[pair] + self.k3

        #print("Plug Delay ", self.plugDelay)
        return self.plugDelay



    def correctPlugVector(self, pdfload):

        '''
        This function calculates the new vector for the plug, based on its  delay that was found in getPlugDelay() and  getPlugNextDelay()
        '''
        
        loadSample = pdfload

        plugNextNoCorrection = loadSample.getNEXT(loadSample.dd, z=True)

        self.minFreq = loadSample.freq[0]
        self.maxFreq = loadSample.freq[-1]
        self.numPoints = len(loadSample.freq)
        
        print("Plug No corr ",plugNextNoCorrection.keys())
        self.correctedPlugVector = {}
        for key in plugNextNoCorrection.keys():
            
            self.correctedPlugVector[key] = []
            
            for f in range(0, len(plugNextNoCorrection[key])):
                #To correct the phase, we must first calculate the old phase
                phase_calib = np.angle(plugNextNoCorrection[key][f], deg=True)
                #Using the old phase and the delay, we will calculate the corrected phase
                phase_corrected = phase_calib + 360 * loadSample.freq[f] * self.plugNextDelay[key]

                '''if(key == "45-36" and loadSample.freq[f] == 100):
                    print("freq: ", loadSample.freq[f])
                    print("Next No corr : ", plugNextNoCorrection[key][f])
                    print("Correct Plug Phase :", phase_corrected)
                    print("Old Plug Phase :", phase_calib)'''
    
                #Then we'll calculate the amplitude
                amplitude = np.abs(plugNextNoCorrection[key][f])

                #By keeping the amplitude the same, we can use the corrected phase to find the new Real and Immaginary components.
                real = amplitude * np.cos(phase_corrected * np.pi/180)
                imag = amplitude * np.sin(phase_corrected * np.pi/180)
                
                #And finally we add the new next with the corrected phase to the corrected plug dictionary
                self.correctedPlugVector[key].append(complex(real, imag))

                '''if(key == "45-36" and loadSample.freq[f] == 100):
                    print("Correct Plug Vect = "+  str(self.correctedPlugVector[key][f]) + "@ pair :" + key)
                    print("Correct Vect: ", complex(real, imag)) '''        
        
        return self.correctedPlugVector


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


    def getDirectFixtureDelay(self, dfopen, dfshort):
        '''
        This function is used to calculate the Delay of the Direct Fixture.
        It must be called before finding the delay of the plug to allow for correction of the delay on the plug
        It finds the average delay of an open measurement and a short measurement on each pair from 100MHZ to 500MHZ. 
        '''
        
        print("Calculating Direct Fixture Delay")

        
        openDelay = self.getDelay(dfopen)
        shortDelay = self.getDelay(dfshort)

        #print("DF Open Delay = ", openDelay["12"][0])
        
        #directFixtureDelay = {} #initialize the DF dictionairy.

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        self.freq = dfopen.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(self.freq)
        for pair in pairs:
            #first Find 100MHz and 500MHz
            f100 = list(dfopen.freq.astype(int)).index(100)
            f500 = list(dfopen.freq.astype(int)).index(500)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500])
            self.directFixtureDelay[pair] = (openAvg + shortAvg)/4


        return self.directFixtureDelay

    def __repr__(self):
        return "Plug"


    def getSample(self, snpfile):
        sample = SNPManipulations(snpfile)       
        sample.s2mm()
        sample.port_name = {0:"45", 1:"12", 2:"36", 3:"78"}
        sample.one_sided = True
        return sample

    def getDelay(self, sample):
        return sample.getPropagationDelay()

        
    def setStandard(self, standard):
        self.standard = standard
        self.worstMargin = {}
        self.worstValue = {}

       # with ProcessPool(cpu_count()) as p:

        for parameter in self.parameters:
            print()
            self.limitmutex.lock()

            self.evaluateLimit(parameter)
                    

            #self.getWorstMargin(parameter.replace(" ", ""))
            #self.getWorstValue(parameter.replace(" ", ""))
            
            self.limitmutex.unlock()


    def evaluateLimit(self, param):
        #print("Evaulating : ", param)

        self.standard.limits[param].evaluateLimit({"f": self.freq} , len(self.freq), neg = True)
        #print("ERROR: Limit Not evaluated", param)
            
