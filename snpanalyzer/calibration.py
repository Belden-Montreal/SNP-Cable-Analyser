class Calibration(object):

    def __init__(self, session):

        self.openMeasured = False
        self.shortMeasured = False
        self.loadMeasured = False
        ports = session.query("SOUR:CAT?").split(',')
        #print(ports)
        self.numPorts = len(ports)
        print("Num ports = ", self.numPorts)
        self.session = session #the communication session must already be opened
        #self.numPorts = session.query("SYST:CHAN:CAT?")
        #print(self.numPorts)
        dut_connector = "\"Null\""

        pairString = ""

        self.doneList = []

        self.lastInstruction = []

        self.session.timeout = 50000000

        for i in range(1, self.numPorts+1):
            for j in range(1, self.numPorts+1):
                if i < j:
                    pairString+= str(i) + "," + str(j) + ","

        pairString = pairString[:-1] #remove last comma
        if self.numPorts == 16:
            pairString = "1,2,1,3,1,4,1,5,1,6,1,7,1,8,1,11,1,12,1,13,1,14,1,11,1,12,1,13,1,14,2,3,2,4,2,5,2,6,2,7,2,8,2,11,2,12,2,13,2,14,3,4,3,5,3,6,3,7,3,8,3,13,3,14,3,15,3,16,4,5,4,6,4,7,4,8,4,13,4,14,4,15,4,16,5,6,5,7,5,8,5,9,5,10,5,15,5,16,6,7,6,8,6,9,6,10,6,15,6,16,7,8,7,9,7,10,7,11,7,12,8,9,8,10,8,11,8,12,9,10,9,11,9,12,9,13,9,14,9,15,9,16,10,11,10,12,10,13,10,14,10,15,10,16,11,12,11,13,11,14,11,15,11,16,12,13,12,14,12,15,12,16,13,14,13,15,13,16,14,15,14,16,15,16"
        for i in range(1, self.numPorts+1):
            self.session.write("SENS:CORR:COLL:GUID:CONN:PORT{} {}".format(i, dut_connector))
        print("done step1")

        for i in range(1, self.numPorts+1):
            self.session.write("SENS:CORR:COLL:GUID:CKIT:PORT{} \'Direct_Fixture\'".format(i))
        print("done step2")
            

        self.session.write("SENS:CORR:COLL:GUID:INIT")
        print("done step3")

        self.session.write("SENS:CORR:COLL:GUID:THRU:PORT {}".format(pairString))
        print("done step4")

        self.session.write("SENS:CORR:COLL:GUID:INIT")
        print("initialized")
        self.session.write("SENS:CORR:COLL:GUID:ISOL ALL")

        print(len(self.session.query("SENS:CORR:COLL:GUID:DESC? 92")))
        print(len("\"Connect NULL TO NULL ADAPTER between port {} and port {}".format(4,13)+"\"\n"))
         
        self.getInstructions()
        
    def getInstructions(self):
        self.instructionList = []
        numSteps = self.session.query("sens:corr:coll:guid:steps?")
        #print "steps aquired"

        #print numSteps + "steps"
        print("get instruction")
        for i in range(1, int(numSteps)+1):
            self.instructionList.append(self.session.query("SENS:CORR:COLL:GUID:DESC? {}".format(i)))
        #print "appended"
        print(self.instructionList)

    def openCalib(self):
        self.lastInstruction = []
        for i in range(1, self.numPorts + 1):
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                
                if "\"Connect NULL OPEN to port "+str(i) +"\"\n" == instruction:
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    print(instruction)
                    self.finished(j)
                    break
            else:
                continue
        self.openMeasured = True
        print("openMeasure =", self.openMeasured)
   #     print(self.session.query("SYST:ACT:MEAS?"))
        print("test")
    def shortCalib(self):
        self.lastInstruction = []
        for i in range(1, self.numPorts + 1):
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                if "\"Connect NULL SHORT to port "+str(i)+"\"\n" == instruction:
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    self.finished(j)
                    break
            else:
                continue
        self.shortMeasured = True

    def loadCalib(self):
        self.lastInstruction = []
        for i in range(1, self.numPorts + 1):
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                if "\"Connect NULL LOAD to port "+str(i)+"\"\n" == instruction:
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    self.finished(j)
                    break
            else:
                continue
        self.loadMeasured = True

    def thruCalib(self, thru):
        self.lastInstruction = []
        for (a,b) in thru:
            #Get index of calibration standard  in the index list
            for j, instruction in enumerate(self.instructionList):
                if "\"Connect NULL TO NULL ADAPTER between port {} and port {}".format(a,b)+"\"\n" == instruction:
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    self.finished(j)
                    break
            else:
                continue
        #print(session.query("SYST:ACT:MEAS?"))


    def redo(self):
        for each in self.lastInstruction:
            self.doneList.remove(each)
            for j, instruction in enumerate(self.instructionList):
                if each == instruction:
                    self.session.write("SENS:CORR:COLL:GUID:ACQ STAN{}".format(j+1))
                    print(instruction)
                    self.finished(j)
                    break
            else:
                continue

    def runCalibrationCMD(self):
        print('''	 \t   PXI M9037A Calibration Wizard\n
		   Follow each instruction precisely to
                   ensure a proper calibration \n\n.
                   Press  Enter to start.''')
        
        _ = input("") #Wait for user to press Enter

        """print('''Insert Open(s) onto VNA end(s).
        Press Enter when you've done so. ''')

        _ = input("") #Wait for user to press Enter
        print("Calibrating Open ...")
        self.openCalib()
        print("Done Calibrating Open\n")

        print('''Insert Short(s) onto VNA end(s).
        Press Enter when you've done so. ''')

        _ = input("") #Wait for user to press Enter
        print("Calibrating Short ...")
        self.shortCalib()
        print("Done Calibrating Short\n")

        print('''Insert Load(s) onto VNA end(s).
        Press Enter when you've done so. ''')"""

        _ = input("") #Wait for user to press Enter
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
                            "seq2":{"end1":[(3,7),(4,8)],   "end2":[(11,15), (12,16)]}},
                      "5A":{"seq1":{"end1":[(1,6), (2,5)],  "end2":[(9,14), (10,13)]},
                            "seq2":{"end1":[(3,8),(4,7)],   "end2":[(11,16), (12,15)]}}}

        thruTwoEnd = {"2B":{"seq1":[(1,11), (2,12)],
                            "seq2":[(3,13), (4,14)],
                            "seq3":[(5,15), (6,16)],
                            "seq4":[(7,9), (8,10)]},
                      "3B":{"seq1":[(1,12), (2,11)],
                            "seq2":[(3,14), (4,13)],
                            "seq3":[(5,16), (6,15)],
                            "seq4":[(7,10), (8,9)]},
                      "4B":{"seq1":[(1,13), (2,14)],
                            "seq2":[(3,15), (4,16)],
                            "seq3":[(5,9), (6,10)],
                            "seq4":[(7,11),(8,12)]},
                      "5B":{"seq1":[(1,14), (2,13)],
                            "seq2":[(3,16), (4,15)],
                            "seq3":[(5,10), (6,9)],
                            "seq4":[(7,12), (8,11)]}}


        #calibrate one end thru
        for attach in thruOneEnd:
            for seq in thruOneEnd[attach]:
                print('''Insert Attatchment {} make connections \n{} - end1\n{} -end2\n\n'''.format(attach, str(thruOneEnd[attach][seq]["end1"]), str(thruOneEnd[attach][seq]["end2"])))
                print("Hit enter when ready to calibrate\n")
                _ = input("") #Wait for user to press Enter
                for end in thruOneEnd[attach][seq]:
                    self.thruCalib(thruOneEnd[attach][seq][end])

        #calibrate 2 end thru
        if(self.numPorts > 8):
            for attach in thruTwoEnd:
                for seq in thruTwoEnd[attach]:
                    print('''Insert Attatchment {} make connections \n{}\n'''.format(attach, str(thruOneEnd[attach][seq])))
                    print("Hit enter when ready to calibrate\n")
                    _ = input("") #Wait for user to press Enter
                    self.thruCalib(thruTwoEnd[attach][seq])
                      
        
    def finished(self, instructionNum):
        self.lastInstruction.append(self.instructionList[instructionNum])
        currentInstruction = self.instructionList[instructionNum]
        #self.instructionList.remove(instructionNum)
        self.doneList.append(currentInstruction)


    def saveCalib(self,calName):
        self.session.query("SENS:CORR:CSET:ITEM:CAT?")
        self.session.write("SENS:CORR:PREF:CSET:SAVE USER")
        self.session.write("SENS:CORR:CSET:NAME '{}'".format(calName))
        print(self.session.query("SENS:CORR:CSET:ITEM:CAT?"))


    def save(self):
        self.session.write("SENS:CORR:COLL:GUID:SAVE 1")
        
    def close(self):
        self.session.write("SENS:CORR:COLL:GUID:ABOR")




if __name__ == "__main__":
    import visa
    import pyvisa
    
    VISA_ADDRESS  = "TCPIP0::10.29.48.46::hislip0::INSTR"

    timeout = 50000
    rm = visa.ResourceManager()
    session = rm.open_resource(VISA_ADDRESS)
    session.timeout = timeout
    print(session.query("*IDN?"))
    print(session.query("SOUR:CAT?"))
            
    cal = Calibration(session)
    cal.getInstructions()
    cal.runCalibrationCMD()
    cal.save()
    cal.close()
