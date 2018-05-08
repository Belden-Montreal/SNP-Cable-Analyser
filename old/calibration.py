import visa
import pyvisa

class Calibration(object):

    def __init__(self, session):

        self.openMeasured = False
        self.shortMeasured = False
        self.loadMeasured = False
        self.numPorts = 16
        
        self.session = session #the communication session must already be opened
        dut_connector = "Null"

        pairString = ""

        self.doneList = []

        self.lastInstruction = []

        for i in range(1, self.numPorts+1):
            for j in range(1, self.numPorts+1):
                if i < j:
                    pairString+= str(i) + "," + str(j) + ","

        pairString = pairString[:-1] #remove last comma

        for i in range(1, numPorts+1):
            self.session.write("SENS:CORR:COLL:GUID:CONN:PORT{} {}").format(i, dut_connector)

        for i in range(1, numPorts+1):
            self.session.write("SENS:CORR:COLL:GUID:CKIT:PORT{} 'Direct_Fixture'").format(i)

        self.session.write("SENS:CORR:COLL:GUID:INIT")

        self.session.write("SENS:CORR:COLL:GUID:THRU:PORT {}").format(pairString)

        self.session.write("SENS:CORR:COLL:GUID:INIT")

        
    def getInstructions(self):
        self.instructionList = []
        numSteps = self.session.query("SENS:CORR:COLL:GUID:STEPS")

        print numSteps + "steps"
        
        for i in range(1, numSteps+1):
            self.instructionList.append(self.session.query("SENS:CORR:COLL:GUID:DESC? {}".format(i)))


    def openCalib(self):
        self.lastInstruction = []
        for i in range(1, self.numPorts + 1):
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(instructionList):
                if "Connect NULL OPEN to port "+i == instruction
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(i))
                    print instruction
                    self.finished(j)
                    break
            else:
                continue
        self.openMeasured = True

    def shortCalib(self):
        self.lastInstruction = []
        for i in range(1, self.numPorts + 1):
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                if "Connect NULL SHORT to port "+i == instruction
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    print instruction
                    break
            else:
                continue
        self.shortMeasured = True

    def loadCalib(self):
        self.lastInstruction = []
        for i in range(1, self.numPorts + 1):
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                if "Connect NULL LOAD to port "+i == instruction
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    print instruction
                    self.finished(j)
                    break
            else:
                continue
        self.loadMeasured = True

    def thruCalib(self, *thru):
        self.lastInstruction = []
        for (a,b) in thru:
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                if "Connect NULL TO NULL ADAPTER between port {} and port {} ".format(a,b) == instruction
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    print instruction
                    self.finished(j)
                    break
            else:
                continue

    def redo(self):
        for each in self.lastInstruction:
            self.doneList.remove(each)
            for j, instruction in enumerate(self.instructionList):
                if each == instruction:
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    print instruction
                    self.finished(j)
                    break
            else:
                continue

    def runCalibrationCMD(self):
        print('''	 \t   PXI M9037A Calibration Wizard\n
		   Follow each instruction precisely to
                   ensure a proper calibration \n\n.
                   Press  Enter to start.''')
        
        _ = raw_input("") #Wait for user to press Enter

        print('''Insert Open(s) onto VNA end(s).
        Press Enter when you've done so. ''')

        _ = raw_input("") #Wait for user to press Enter
        print("Calibrating Open ...")
        self.openCalib()
        print("Done Calibrating Open")

        print('''Insert Short(s) onto VNA end(s).
        Press Enter when you've done so. ''')

        _ = raw_input("") #Wait for user to press Enter
        print("Calibrating Short ...")
        self.shortCalib()
        print("Done Calibrating Short")

        print('''Insert Load(s) onto VNA end(s).
        Press Enter when you've done so. ''')

        _ = raw_input("") #Wait for user to press Enter
        print("Calibrating Load ...")
        self.loadCalib()
        print("Done Calibrating Load\n\n")

        #Define thru sequences in a dictioniary              
        thruOneEnd = {"1A":{"seq1":{"end1":[(1,2), (3,4), (5,6), (7,8)],"end2":[(9,10), (11,12), (13,14), (15,16)]}},
                      "2A":{"seq1":{"end1":[(1,3), (2,4)],  "end2":[(9,11), (10,12)]},
                            "seq2":{"end1":[(3,5),(4,6)],   "end2":[(11,13), (12,14)]},
                            "seq3":{"end1":[(5,7), (6,8)],  "end2":[(13,15), (14,16)]},
                            "seq4":{"end1":[(1,7), (2,8)],  "end2":[(9,15), (10,16)]}},
                      "3A":{"seq1":{"end1":[(1,4), (2,3)],  "end2":[(9,12), (10,11)]},
                            "seq2":{"end1":[(3,6),(4,5)],   "end2":[(11,14), (12,13)]},
                            "seq3":{"end1":[(5,8), (6,7)],  "end2":[(13,16), (14,15)]},
                            "seq4":{"end1":[(1,8), (2,7)],  "end2":[(9,16), (10,15)]}},
                      "4A":{"seq1":{"end1":[(1,5), (2,6)],  "end2":[(9,13), (10,14)]},
                            "seq2":{"end1":[(3,7),(4,8)],   "end2":[(11,15), (12,16)]}}
                      "5A":{"seq1":{"end1":[(1,6), (2,5)],  "end2":[(9,14), (10,13)]},
                            "seq2":{"end1":[(3,8),(4,7)],   "end2":[(11,16), (12,15)]}}}

        thruTwoEnd = {"2B":{"seq1":[(1,11), (2,12)],
                            "seq2":[(3,13), (4,14)],
                            "seq3":[(5,15), (6,16)],
                            "seq4":[(7,9), (8,10)]},
                      "3B":{"seq1":[(1,12), (2,11)],
                            "seq2":[(3,14), (4,13)],
                            "seq3":[(5,16), (6,15)],
                            "seq4":[(7,10), (8,9)]}
                      "4B":{"seq1":[(1,13), (2,14)],
                            "seq2":[(3,15), (4,16)],
                            "seq3":[(5,9), (6,10)],
                            "seq4":[(7,11),(8,12)]},
                      "5B":{"seq1":[(1,14), (2,13)],
                            "seq2":[(3,16), (4,15)],
                            "seq3":[(5,10), (6,9)],
                            "seq4":[(7,12), (8,11)]}}


        #calibrate one end thru
        for attatch in thruOneEnd:
            for seq in thruOneEnd[attach]:
                print('''Insert Attatchment {} make connections \n{} - end1\n{} -end2\n\n'''.format(attach, str(thruOneEnd[attach][seq]["end1"]), str(thruOneEnd[attach][seq]["end2"])))
                print("Hit enter when ready to calibrate")
                _ = raw_input("") #Wait for user to press Enter
                for end in thruOneEnd[attach][seq]:
                    self.thruCalib(end)

        #calibrate 2 end thru
        for attatch in thruTwoEnd:
            for seq in thruTwoEnd[attach]:
                print('''Insert Attatchment {} make connections \n{}\n'''.format(attach, str(thruOneEnd[attach][seq]))
                print("Hit enter when ready to calibrate")
                _ = raw_input("") #Wait for user to press Enter
                self.thruCalib(seq)
                      
        
    def finished(self, instructionNum):
        self.lastInstruction.append(self.instructionList[instructionNum])
        currentInstruction = self.instructionList[instructionNum]
        #self.instructionList.remove(instructionNum)
        self.doneList.append(currentInstruction)

    def save(self):
        self.session.write("SENS:CORR:COLL:GUID:SAVE 1")
        
    def close(self):
        self.session.write("SENS:CORR:COLL:GUID:ABOR")


if __name__ == "__main__":
    cal = Calibration()

