from snpAnalyze import SNPManipulations
import numpy as np
import os
import json

import xlsxwriter
import sympy

class Embedding(SNPManipulations):

    def __init__(self):

        self.directFixtureDelay = {}
        self.plugDelay = {}
        self.plugNextDelay = {}
        self.plugJackDelay = {}
        self.jackDelay = {}
        self.correctedPlugVector = {}
        self.testName = "DEEMBED_1"
        self.plugName = "TestPlug"
        self.jackName = "TestJack"

        self.workbook = xlsxwriter.Workbook(self.testName+".xlsx")


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

        print("OK")

        self.openSample = openSNP
        self.shortSample = shortSNP
        
        openDelay = self.getOpenDelay()
        shortDelay = self.getShortDelay()

        print("DF Open Delay = ", openDelay["12"][0])
        
        #directFixtureDelay = {} #initialize the DF dictionairy.

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        freq = self.openSample.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(freq)
        for pair in pairs:
            #first Find 100MHz and 500MHz
            f100 = list(self.openSample.freq).index(100400400.4004)
            f500 = list(self.openSample.freq).index(500000000)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500])
            self.directFixtureDelay[pair] = (openAvg + shortAvg)/4


        return self.directFixtureDelay


    def getPlugDelay(self, openSNP, shortSNP):

        self.openSample = openSNP
        self.shortSample = shortSNP
        
        openDelay = self.getOpenDelay()
        shortDelay = self.getShortDelay()

        pairs = openDelay.keys() #Get list of pairs (This is the same as shortDelay)
        freq = self.openSample.freq   #Get the list of frequencies (This is the same as the shortSample)
        num_samples = len(freq)
               
        for pair in pairs:
            f100 = list(self.openSample.freq).index(100400400.4004)
            f500 = list(self.openSample.freq).index(500000000)
            print("f100 ", f100)
            openAvg = np.mean(openDelay[pair][f100:f500])
            shortAvg = np.mean(shortDelay[pair][f100:f500]) + 85e-12


            self.plugDelay[pair] = ((openAvg + shortAvg)/4) - self.directFixtureDelay[pair]

            
        return self.plugDelay
    

    def getPlugNextDelay(self):
        print("plugDelay Keys: ", self.plugDelay.keys())

        self.plugNextDelay["12-36"] = self.plugDelay["12"] + self.plugDelay["36"]
        self.plugNextDelay["45-12"] = self.plugDelay["12"] + self.plugDelay["45"]
        self.plugNextDelay["12-78"] = self.plugDelay["12"] + self.plugDelay["78"]
        self.plugNextDelay["45-36"] = self.plugDelay["36"] + self.plugDelay["45"]
        self.plugNextDelay["36-78"] = self.plugDelay["36"] + self.plugDelay["78"]
        self.plugNextDelay["45-78"] = self.plugDelay["45"] + self.plugDelay["78"]

        return self.plugNextDelay
    

    def correctPlugVector(self, loadSNP):
        
        self.loadSample = loadSNP

        plugNextNoCorrection = self.loadSample.getNEXT(self.loadSample.dd, z=True)
        print("Plug No corr ",plugNextNoCorrection.keys())
        self.correctedPlugVector = {}
        for key in plugNextNoCorrection.keys():
            
            self.correctedPlugVector[key] = []
            for f in range(0, len(plugNextNoCorrection[key])):
                #To correct the phase, we must first calculate the old phase
                phase_old = np.angle(plugNextNoCorrection[key][f], deg=True)
                #Using the old phase and the delay, we will calculate the corrected phase
                phase_corrected = phase_old + 360 * self.loadSample.freq[f] * self.plugNextDelay[key]

                if(key == "45-36" and self.loadSample.freq[f]== 100400400.4004):
                    print("freq: ", self.loadSample.freq[f])
                    print("Next No corr : ", plugNextNoCorrection[key][f])
                    print("Correct Plug Phase :", phase_corrected)
                    print("Old Plug Phase :", phase_old)
    
                #Then we'll calculate the amplitude
                amplitude = np.abs(plugNextNoCorrection[key][f])

                #By keeping the amplitude the same, we can use the corrected phase to find the new Real and Immaginary components.
                real = amplitude * np.cos(phase_corrected * np.pi/180)
                imag = amplitude * np.sin(phase_corrected * np.pi/180)




                #And finally we add the new next with the corrected phase to the corrected plug dictionary
                self.correctedPlugVector[key].append((real, imag))

                if(key == "45-36" and self.loadSample.freq[f] == 100400400.4004):
                    print("Correct Plug Vect = "+  str(self.correctedPlugVector[key][f]) + "@ pair :" + key)
                    print("Correct Vect: ", complex(real, imag))         


        #print("Correct Plug Vect = "+  str(self.correctedPlugVector[key][0]) + "@ pair :" + key)
                
        #And then we write the corrected Next dictionary to a json file
        testPlugFile = open(self.plugName ,"w")
        testPlugFile.write(json.dumps(self.correctedPlugVector))
        testPlugFile.close


        '''WRTIE TO EXCEL DB'''

        worksheet = self.workbook.add_worksheet("Plug Corrected DB Phase")


        cell_format = self.workbook.add_format({'align': 'center',
                                               'valign': 'vcenter'})
        worksheet.merge_range('B1:C1', "", cell_format)
        worksheet.merge_range('D1:E1', "", cell_format)
        worksheet.merge_range('F1:G1', "", cell_format)
        worksheet.merge_range('H1:I1', "", cell_format)
        worksheet.merge_range('J1:K1', "", cell_format)
        worksheet.merge_range('L1:M1', "", cell_format)

        worksheet.write('A2', "Frequency")
        for i, f in enumerate(self.loadSample.freq):
            worksheet.write(i+2,0, f)

        curPos = 1
        for i, key in enumerate(self.correctedPlugVector.keys()):
            print(key)

            worksheet.write(0, curPos, key)
            worksheet.write(1, curPos, "dB")
            worksheet.write(1, curPos+1, "⌀")

            for f in range(0, len(self.correctedPlugVector[key])):
                
                worksheet.write(2+f,curPos, 20 * np.log10(np.sqrt(self.correctedPlugVector[key][f][0]**2 +self.correctedPlugVector[key][f][1]**2 )))
                worksheet.write(2+f,curPos+1, np.angle(complex(self.correctedPlugVector[key][f][0], self.correctedPlugVector[key][f][1]),deg=True))

            curPos += 2

        '''WRTIE TO EXCEL REAL IMAG'''

        worksheet = self.workbook.add_worksheet("Plug Corrected Z")


        cell_format = self.workbook.add_format({'align': 'center',
                                               'valign': 'vcenter'})
        worksheet.merge_range('B1:C1', "", cell_format)
        worksheet.merge_range('D1:E1', "", cell_format)
        worksheet.merge_range('F1:G1', "", cell_format)
        worksheet.merge_range('H1:I1', "", cell_format)
        worksheet.merge_range('J1:K1', "", cell_format)
        worksheet.merge_range('L1:M1', "", cell_format)

        worksheet.write('A2', "Frequency")
        for i, f in enumerate(self.loadSample.freq):
            worksheet.write(i+2,0, f)

        curPos = 1
        for i, key in enumerate(self.correctedPlugVector.keys()):
            print(key)

            worksheet.write(0, curPos, key)
            worksheet.write(1, curPos, "Re")
            worksheet.write(1, curPos+1, "Im")

            for f in range(0, len(self.correctedPlugVector[key])):
                
                worksheet.write(2+f,curPos, self.correctedPlugVector[key][f][0])
                worksheet.write(2+f,curPos+1,  self.correctedPlugVector[key][f][1])

            curPos += 2
        
        return self.correctedPlugVector
    

    def getJackVector(self, loadSNP):
        
        #This function takes in the SNP of the mated maesurment (Jack + Test Plug)
        #and extracts the Jack Vector
        
        self.loadSample = loadSNP       #Mated sample

        matedNext = self.loadSample.getNEXT(self.loadSample.dd, z=True)

        self.jackVector = {}

        for key in matedNext.keys():
            self.jackVector[key] = []
            for f in range(0, len(matedNext[key])):

                self.jackVector[key].append(matedNext[key][f] - complex(self.correctedPlugVector[key][f][0], self.correctedPlugVector[key][f][1] ))

                

                
        #And then we write the corrected jack Next dictionary to a json file
        print(self.jackVector["12-36"][2])
        print()
        #testPlugFile = open(self.jackName, "w")
        #testPlugFile.write(json.dumps(self.jackVector))
        #testPlugFile.close

        '''WRTIE TO EXCEL DB'''

        worksheet = self.workbook.add_worksheet("Jack Corrected DB Phase")


        cell_format = self.workbook.add_format({'align': 'center',
                                               'valign': 'vcenter'})
        worksheet.merge_range('B1:C1', "", cell_format)
        worksheet.merge_range('D1:E1', "", cell_format)
        worksheet.merge_range('F1:G1', "", cell_format)
        worksheet.merge_range('H1:I1', "", cell_format)
        worksheet.merge_range('J1:K1', "", cell_format)
        worksheet.merge_range('L1:M1', "", cell_format)

        worksheet.write('A2', "Frequency")
        for i, f in enumerate(self.loadSample.freq):
            worksheet.write(i+2,0, f)

        curPos = 1
        for i, key in enumerate(self.jackVector.keys()):
            print(key)

            worksheet.write(0, curPos, key)
            worksheet.write(1, curPos, "dB")
            worksheet.write(1, curPos+1, "⌀")

            for f in range(0, len(self.jackVector[key])):
                
                worksheet.write(2+f,curPos, 20 * np.log10(np.abs(self.jackVector[key][f])))
                worksheet.write(2+f,curPos+1, np.angle(self.jackVector[key][f]))

            curPos += 2

        '''WRTIE TO EXCEL REAL IMAG'''

        worksheet = self.workbook.add_worksheet("Jack Corrected Z")


        cell_format = self.workbook.add_format({'align': 'center',
                                               'valign': 'vcenter'})
        worksheet.merge_range('B1:C1', "", cell_format)
        worksheet.merge_range('D1:E1', "", cell_format)
        worksheet.merge_range('F1:G1', "", cell_format)
        worksheet.merge_range('H1:I1', "", cell_format)
        worksheet.merge_range('J1:K1', "", cell_format)
        worksheet.merge_range('L1:M1', "", cell_format)

        worksheet.write('A2', "Frequency")
        for i, f in enumerate(self.loadSample.freq):
            worksheet.write(i+2,0, f)

        curPos = 1
        for i, key in enumerate(self.jackVector.keys()):
            print(key)

            worksheet.write(0, curPos, key)
            worksheet.write(1, curPos, "Re")
            worksheet.write(1, curPos+1, "Im")

            for f in range(0, len(self.jackVector[key])):
                
                worksheet.write(2+f,curPos, self.jackVector[key][f].real)
                worksheet.write(2+f,curPos+1,  self.jackVector[key][f].imag)

            curPos += 2
        self.workbook.close()
        
        return self.jackVector

'''    def setLimit(self, cat):

        if cat == "6A" or cat == "6":
            self.case1  = lambda f: 38.1-20*np.log(f/100)
            self.case2  = lambda f: 38.6-20*np.log(f/100)
            self.case3  = lambda f: 39.0-20*np.log(f/100)
            self.case4  = lambda f: 39.5-20*np.log(f/100)
            self.case5  = lambda f: 46.5-20*np.log(f/100)
            self.case6  = lambda f: 49.5-20*np.log(f/100)
            self.case7  = lambda f: 46.5-20*np.log(f/100)
            self.case8  = lambda f: 49.5-20*np.log(f/100)
            self.case9  = lambda f: 57.0-20*np.log(f/100)
            self.case10 = lambda f: 70.0-20*np.log(f/100)
            self.case11 = lambda f: 57.0-20*np.log(f/100)
            self.case12 = lambda f: 70.0-20*np.log(f/100)
            self.case13 = lambda f: 66.0-20*np.log(f/100)
            self.case14 = lambda f: 66.0-20*np.log(f/100)
            
        elif cat == "5":
            self.case1  = lambda f: 35.8- 20 * np.log(f/100)
            self.case2  = ([], [])
            self.case3  = ([], [])
            self.case4  = lambda f: 39.5- 20 * np.log(f/100)
            self.case5  = lambda f: 42.0- 20 * np.log(f/100)
            self.case6  = lambda f: 50.0- 20 * np.log(f/100)
            self.case7  = lambda f: 42.0- 20 * np.log(f/100)
            self.case8  = lambda f: 50.0- 20 * np.log(f/100)
            self.case9  = lambda f: 50.0- 20 * np.log(f/100)
            self.case10 = ([],[])
            self.case11 = lambda f: 50.0- 20 * np.log(f/100)
            self.case12 = ([], [])
            self.case13 = lambda f: 60.0- 20 * np.log(f/100)
            self.case14 = ([], [])
            
    def reembed(self):
        
        self.setLimit("6A")
        self.reMated = {}
        for f in self.freq: 
        for i in range(1,14):
            #First, we will 
            self.reMated[1] = 
'''

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
    plugDirectFixtureLoad = "snps\DEEMBED TEST\DirectFixPlug.s8p"

    plugJackLoad = "snps\DEEMBED TEST\MatingPlugJackForward.s8p"

    em.getDirectFixtureDelay(directFixtureOpen, directFixtureShort)
    em.getPlugDelay(plugDirectFixtureOpen, plugDirectFixtureShort)
    em.getPlugNextDelay()
    em.correctPlugVector(plugDirectFixtureLoad)
    em.getJackVector(plugJackLoad)
    
    

    

    

    
