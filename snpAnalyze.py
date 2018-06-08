import pylab
from skrf import Network as rf

import numpy as np
from scipy.misc import derivative
class SNPManipulations(rf):

    def __init__(self, snpFile):
        self.rs = super(SNPManipulations, self)
        self.rs.__init__(snpFile)
        
        #self.sMat = self.rs.s   #Scattering parameter matrix.
        #self.zMat = self.rs.z   #Impedance parameter matrix.
        self.freq = np.array(self.f)   #Array containing all frequency
        self.se = self.s #single ended

        self.num_ports = self.rs.number_of_ports
        self.num_samples = len(self.f)

        #create an inital dictionairy of port names {portNumber : portName}
        #ex: port_names = {0: '1', 1: '2', 2: '3', 3:'4'}.
        #This can be modified.
        self.port_name = {i:str(i+1) for i in range(0,self.num_ports)}
        self.one_sided = False
        self.freq_unit = 'mhz'

    def getRL(self, matrix, z=True ):
        '''
        Get the Return Loss array in dd or cc mode.
        Use this function to get LCL in dc mode or TCL in cd mode.

        Parameters :  z : If True, returns complex values. If False, returns polar coordinates. Default = True
                      matrix: Specifie the matrix (se, dd, dc, cd ,dd) that you wish to extract the RLfrom (by default its the single ended matrix se)
                             

        Returns: Dictionairy containing each RL value in an array for each frequency. 

        Ex: SNPManipulations.getRL()
            >>>  {"RL_11: [RL_1 @ f1, RL_1 @ f2, RL_1 @ f3]"},
                  "RL_22: [RL_2 @ f1, RL_2 @ f2, RL_2 @ f3]"}, ...        
        '''
        
        #initialize RL dictionairy
        self.RL_dict = {}
        numPorts = self.getNumPorts(matrix)
        
        #Establish dicitonairy keys and initialize arrays
        for i in range(0, numPorts):
            self.RL_dict[self.port_name[i]] = []
            
        #Populate dictionairy
        for f in range(0, self.num_samples):
            for j in range(0, numPorts):
                rlVal = matrix[f, j, j]
                #Convert to polar coordinates (Mag, Phase)                
                if(z == False):
                    rlVal = self.complex2db(rlVal)   #(Mag_dB, phase)
                #self.RL_dict["RL_" + str(j) + str(j)].append(rlVal)
                self.RL_dict[self.port_name[j]].append(rlVal)
        return self.RL_dict

    def getIL(self, matrix, z=True, full=False):
        '''
        Get the Insertion Loss array in dd or cc mode.
        Use this function to get LCTL in dc mode or TCTL in cd mode.

        Parameters :  z : If True, returns complex values. If False, returns polar coordinates. Default = True

        Returns: Dictionairy containing each IR value in an array for each frequency. 

        Ex: SNPManipulations.getIL()
            >>>  {"IL_13: [IL_1-3 @ f1, IL_1-3 @ f2, IL_1-3 @ f3 ... ]"},
                  "IL_24: [IL_2-4 @ f1, IL_2-4 @ f2, IL_3-4 @ f3 ... ]"}, ... 
        '''
        
        #initialize IL dictionairy
        self.IL_dict = {}
        numPorts = self.getNumPorts(matrix)
         

        if self.one_sided: #if the test setup is one sided, then there can be no
                           #insertion loss because there is no other side for
                           #the signal to go through
            return {}
            
        
        #Establish dicitonairy keys and initialize arrays
        for i in range(0, numPorts//2):
            self.IL_dict[self.port_name[i]] = []
            if full is True:
                self.IL_dict[self.port_name[i+numPorts//2]] = [] 

        #print self.IL_dict.keys()
        #Populate dictionairy
        for f in range(0, self.num_samples):           
            
            for j in range(0, numPorts//2):
                topRight = matrix[f, j, j+numPorts//2]
                if full is True:
                    bottomLeft = matrix[f,j+numPorts//2, j]

                #Convert to polar coordinates (Mag, Phase)                
                if(z == False):
                    topRight = self.complex2db(topRight)
                    if full is True:
                        bottomLeft = self.complex2db(bottomLeft)    
                self.IL_dict[str(self.port_name[j])].append(topRight)
                if full is True:
                    self.IL_dict[self.port_name[j+numPorts//2]].append(bottomLeft)

                

        return self.IL_dict


    def getNEXT(self, matrix, z=True):
        '''
        Get the Near-End Cross Talk array
        
        Parameters :  z : If True, returns complex values. If False, returns polar coordinates. Default = True

        Returns: Numpy array containing all NEXT values at each frequency value

        Ex: SNPManipulations.getIL()
            >>>  {"NEXT_21: [NEXT_21 @ f1, NEXT_21 @ f2, NEXT_21 @ f3 ... ]"},
                  "NEXT_12: [NEXT_12 @ f1, NEXT_12 @ f2, NEXT_12 @ f3 ... ]"}, ... 
       
        '''

        #initialize IL dictionairy
        self.NEXT_dict = {}
        numPorts = self.getNumPorts(matrix)

        if not self.one_sided:
            #print "doing"
            #Establish dicitonairy keys and initialize arrays
            for i in range(0, numPorts//2):
                for j in range (0, numPorts//2):
                    if i < j:
                        self.NEXT_dict[self.port_name[i] + "-" + self.port_name[j]] = []
                        self.NEXT_dict[self.port_name[i + numPorts//2] + "-" + self.port_name[j + numPorts//2]] = []

            #Populate dictionairy
            for f in range(0, self.num_samples):
                for i in range(0, numPorts//2):
                    for j in range (0, numPorts//2):
                        if i < j:
                            topLeft = matrix[f, i, j]
                            bottomRight = matrix[f, i+numPorts//2, j+numPorts//2]
                            if(z == False):
                                #Convert to polar coordinates (Mag, Phase)
                                topLeft = self.complex2db(matrix[f, i, j])
                                bottomRight = self.complex2db(matrix[f, i+numPorts//2, j+numPorts//2]) 
                                
                            self.NEXT_dict[self.port_name[i] + "-" + self.port_name[j]].append(topLeft)
                            self.NEXT_dict[self.port_name[i + numPorts//2] + "-" + self.port_name[j + numPorts//2]].append(bottomRight)

            return  self.NEXT_dict

        #Establish dicitonairy keys and initialize arrays
        for i in range(0, numPorts):
            for j in range (0, numPorts):
                if i < j:
                    self.NEXT_dict[self.port_name[i] + "-" + self.port_name[j]] = []

        #Populate dictionairy
        for f in range(0, self.num_samples):
            for i in range(0, numPorts):
                for j in range (0, numPorts):
                    if i < j:
                        m = matrix[f, i, j]
                        bottomLeft = m
                        if(z == False):
                        #Convert to polar coordinates (Mag, Phase)
                            bottomLeft = self.complex2db(m) 
                            
                        self.NEXT_dict[self.port_name[i] + "-" + self.port_name[j]].append(bottomLeft)

            
        return self.NEXT_dict 

    def getFEXT(self, matrix, z=True):
        '''
        Get the Far-End Cross Talk array
        
        Parameters : z : If True, returns complex values. If False, returns polar coordinates. Default = True

        Returns: Numpy array containing all FEXT values at each frequency value

        Ex: SNPManipulations.getIL()
            >>>  {"FEXT_41: [FEXT_41 @ f1, FEXT_41 @ f2, FEXT_41 @ f3 ... ]"},
                  "FEXT_14: [FEXT_14 @ f1, FEXT_14 @ f2, FEXT_14 @ f3 ... ]"}, ... 
       
        '''
        #initialize IL dictionairy
        self.FEXT_dict = {}
        numPorts = self.getNumPorts(matrix)
        if self.one_sided: #if the test setup is one sided, then there can be no
                           #insertion loss because there is no other side for
                           #the signal to go through
            return {}

        #Establish dicitonairy keys and initialize arrays
        for i in range(numPorts//2, numPorts):
            for j in range (0, numPorts//2):
                #print str(j)

                if i != j and abs(i-j) != (numPorts//2):
                    self.FEXT_dict[self.port_name[i] + "-" + self.port_name[j]] = []
                    self.FEXT_dict[self.port_name[j] + "-" + self.port_name[i]] = []
        #return self.FEXT_dict

        #Populate dictionairy
        for f in range(0, self.num_samples):
            for i in range(numPorts//2, numPorts):
                for j in range (0,numPorts//2):
                    #print str(j)

                    if i != j and abs(i-j) != (numPorts/2):
                        bottomLeft = matrix[f, i, j]
                        topRight = matrix[f, j, i]
                        if(z == False):
                            #Convert to polar coordinates (Mag, Phase)
                            bottomLeft = self.complex2db(bottomLeft) 
                            topRight =  self.complex2db(topRight) 
                        
                        self.FEXT_dict[self.port_name[i] + "-" + self.port_name[j]].append(bottomLeft)
                        self.FEXT_dict[self.port_name[j] + "-" + self.port_name[i]].append(topRight)

        return self.FEXT_dict


    def getPSNEXT(self, matrix):
        NEXT_db = self.getNEXT(matrix, z=False) #First, we start by calculating the NEXT in db. We do this regardless of wether it has already been done.

        self.PSNEXT_dict = {}
        numPorts = self.getNumPorts(matrix)
        #Establish dicitonairy keys and initialize arrays
        for k in range(0, numPorts):
                #print str(j)
            self.PSNEXT_dict[self.port_name[k]] = []

        #Populate dictionairy
        #self.PSNEXT_dict[self.port_name[0]] = []

        for f in range(0, self.num_samples):
            for k in range(0, numPorts):
                keys = NEXT_db.keys()
                PSk = 10*np.log10(np.sum([10**(NEXT_db[key][f]/10) for key in keys if (key.split("-")[0] == self.port_name[k] or key.split("-")[1] == self.port_name[k]) ]))
                self.PSNEXT_dict[self.port_name[k]].append(PSk)
                    


                #PSNEXT_side2 = 10*np.log10(np.sum([10**-(NEXT_db[self.port_name[k+numPorts/2] + "-" + self.port_name[i]])/10 for i in range(numPorts/2, numPorts) if i < k]))
                #self.PSNEXT_dict[self.port_name[k+numPorts/2]].append(PSNEXT_side2)


            
        return self.PSNEXT_dict


    def getPSFEXT(self, matrix):

        if self.one_sided: #if the test setup is one sided, then there can be no
                           #FEXT  because there is no other side for
                           #the signal to go through
            return {}
            
        FEXT_db = self.getFEXT(matrix, z=False) #First, we start by calculating the FEXT in db. We do this regardless of wether it has already been done.

        self.PSFEXT_dict = {}
        numPorts = self.getNumPorts(matrix)
        #Establish dicitonairy keys and initialize arrays
        for k in range(0, numPorts):
            self.PSFEXT_dict[self.port_name[k]] = []

        #Populate dictionairy
        #self.PSNEXT_dict[self.port_name[0]] = []
        keys = FEXT_db.keys()

        for f in range(0, self.num_samples):
            for k in range(0, numPorts):
                PSk = 10*np.log10(np.sum([10**(FEXT_db[key][f]/10) for key in keys if (key.split("-")[0] == self.port_name[k] ) ]))
                self.PSFEXT_dict[self.port_name[k]].append(PSk)
                    
                #PSNEXT_side2 = 10*np.log10(np.sum([10**-(NEXT_db[self.port_name[k+numPorts/2] + "-" + self.port_name[i]])/10 for i in range(numPorts/2, numPorts) if i < k]))
                #self.PSNEXT_dict[self.port_name[k+numPorts/2]].append(PSNEXT_side2)


        #print len(self.PSFEXT_dict["12"].values())
        return self.PSFEXT_dict


    def getACRF(self, matrix):
        '''
        The caluclaation of the ACRF is simply the subtraction of the FEXT and IL.
        To do this, I will simply take each FEXT that has been calculated, extract the disturbed pair (k),
        and subract by IL_k.
        '''

        if self.one_sided: #if the test setup is one sided, then there can be no
                           #ACRF  because there is no other side for
                           #the signal to go through
            return {}
            
        
        FEXT_db = self.getFEXT(matrix, z=False) #First, we start by calculating the FEXT in db. We do this regardless of wether it has already been done.
        IL_db = self.getIL(matrix, z=False, full=True) #First, we start by calculating the IL in db. We do this regardless of wether it has already been done.


        FEXT_keys = FEXT_db.keys()
        
        self.ACRF_dict = {}
        numPorts = self.getNumPorts(matrix)
        #Establish dicitonairy keys and initialize arrays
        for key in FEXT_keys:
            #print str(j)
            self.ACRF_dict[key] = []

        #Populate dictionairy
        #self.PSNEXT_dict[self.port_name[0]] = []

        for f in range(0, self.num_samples):
            for key in FEXT_keys:
                k = key.split("-")[0]
                ACRFk = FEXT_db[key][f] - IL_db[k][f]
                self.ACRF_dict[key].append(ACRFk)       
        

        return self.ACRF_dict

    def getPSACRF(self, matrix):

        '''self.PSACRF_dict = {}
        PSFEXT = self.getPSFEXT(matrix)

        #Then we get a list of all the port names as well as a list of all the ACRF names
        port_names = [names for names in self.port_name.values()]
        PSFEXT_names = [names for names in ACRF.keys()]

        #We establish dicitonairy keys and initialize arrays
        for k in port_names:
            #print str(j)
            self.PSACRF_dict[k] = []

        #We calculate for each frequency
        for f in range(0, self.num_samples):
            for k in port_names:
                #We create a list of ACRFs that disturbed on port k. 
                ACRF_k = [ACRF[i][f] for i in ACRF if i.split("-")[0] == k]
                #print ACRF_k
                PSACRF_k = np.sum(ACRF_k)
                self.PSACRF_dict[k].append(PSACRF_k)'''
        if self.one_sided: #if the test setup is one sided, then there can be no
                           #ACRF  because there is no other side for
                           #the signal to go through
            return {}
            
        
        PSFEXT_db = self.getPSFEXT(matrix) #First, we start by calculating the FEXT in db. We do this regardless of wether it has already been done.
        IL_db = self.getIL(matrix, z=False, full=True) #First, we start by calculating the IL in db. We do this regardless of wether it has already been done.

        print(IL_db.keys())
        PSFEXT_keys = PSFEXT_db.keys()
        
        self.PSACRF_dict = {}
        numPorts = self.getNumPorts(matrix)
        #Establish dicitonairy keys and initialize arrays
        for key in PSFEXT_keys:
            #print str(j)
            self.PSACRF_dict[key] = []

        #Populate dictionairy
        #self.PSNEXT_dict[self.port_name[0]] = []

        for f in range(0, self.num_samples):
            for key in PSFEXT_keys:
                PSACRFk =PSFEXT_db[key][f] - IL_db[key][f]
                self.PSACRF_dict[key].append(PSACRFk)     

        return self.PSACRF_dict



    """
    def getACRN(self, matrix):
        '''
        The caluclaation of the ACRN is simply the subtraction of the NEXT and IL.
        To do this, I will simply take each NEXT that has been calculated, extract the disturbed pair (k),
        and subract by IL_k.
        '''

        if self.one_sided: #if the test setup is one sided, then there can be no
                           #ACRF  because there is no other side for
                           #the signal to go through
            return {}
            
        
        NEXT_db = self.getNEXT(matrix, z=False) #First, we start by calculating the NEXT in db. We do this regardless of wether it has already been done.
        IL_db = self.getIL(matrix, z=False, full=True) #First, we start by calculating the IL in db. We do this regardless of wether it has already been done.


        NEXT_keys = NEXT_db.keys()
        
        self.ACRN_dict = {}
        numPorts = self.getNumPorts(matrix)
        #Establish dicitonairy keys and initialize arrays
        for key in NEXT_keys:
            #print str(j)
            self.ACRN_dict[key] = []

        #Populate dictionairy
        #self.PSNEXT_dict[self.port_name[0]] = []

        for f in range(0, self.num_samples):
            for key in NEXT_keys:
                k = key.split("-")[0]
                ACRFk = FEXT_db[key][f] - IL_db[k][f]
                self.ACRF_dict[key].append(ACRFk)       
        

        return self.ACRF_dict
    """

    def getELTCTL(self):

        self.ELTCTL_dict = {}
        IL = self.getIL(self.dd, z=False)
        TCTL = self.getIL(self.cd, z=False)

        port_names = [key for key in IL.keys()]

        #We establish dicitonairy keys and initialize arrays
        for key in port_names:
            #print str(j)
            self.ELTCTL_dict[key] = []

        #We calculate for each frequency
        for f in range(0, self.num_samples):
            for k in port_names:
                #We create a list of ACRFs that disturbed on port k. 
                ELTCTL_k = TCTL[k][f] - IL[k][f]
                self.ELTCTL_dict[k].append(ELTCTL_k)

        return self.ELTCTL_dict

    
    def getPropagationDelay(self):

        self.DELAY_dict = {}
        RL = self.getRL(self.dd, z=True)
        
        
        port_names = [key for key in RL.keys()]

        #We establish dicitonairy keys and initialize arrays
        for key in port_names:
            #print str(j)
            self.DELAY_dict[key] = []

        phase = []
        
        '''
        #We calculate for each frequency
        #for f in range(0, self.num_samples):
        for k in port_names:
            #We create a list of propagation delays that disturbed on port k.
            for f in range(0, self.num_samples):
                phase.append(self.complex2phase(RL[k][f]))

            print("pK @ 1G=" , phase[1000-1])
            print(len(self.freq))
            z = np.polyfit(self.freq, phase , 30)
            phase = np.poly1d(z)
            print("pK @ 1G=" , phase(1e9))

            print(phase)
            for f in range(0, self.num_samples):
                freq = self.freq[f]
                dp = derivative(phase, freq, dx = 30000)
                DELAY_k = (-1/360) * dp
                self.DELAY_dict[k].append(DELAY_k)
            phase = []
            print(dp)
            print("freq= ", freq)

        print(self.DELAY_dict["12"][1000-1])
        '''


        #We calculate for each frequency
        print(self.freq[-1])
        for f in range(0, self.num_samples):
            for k in port_names:
      
                try:
                    if self.freq[f] != self.freq[-1]:  #if not last frequency
                        phase1 = self.complex2phase(RL[k][f])
                        phase2 = self.complex2phase(RL[k][f+1])

                        dp = phase2 - phase1
                        df = self.freq[f+1] - self.freq[f]
                        DELAY_k = (-1/360) * dp/df
                        if DELAY_k < 0.0:
                            DELAY_k = self.DELAY_dict[k][f-1]
                        self.DELAY_dict[k].append(DELAY_k)

                    else:
                        DELAY_k = self.DELAY_dict[k][f-1]
                        self.DELAY_dict[k].append(DELAY_k)

                except Exception as e:
                    DELAY_k = 0.0
                    self.DELAY_dict[k].append(DELAY_k)
                    print(self.freq[f])
                    print(e)
                
                
        
        return self.DELAY_dict



    def complex2db(self, zIn, deg=True):
        '''
        Convert Complex number to dB and phase
        
        Parameters : zIn : Complex input (np.array[Re, Im])

        Returns: Tuple of dB and Phase (db, Phase)       
        '''
        
        try:
            return 20*np.log10(np.abs(zIn))
        except Exception as e:
            print(e)

    def complex2phase(self, zIn, deg=True):
        '''
        Convert Complex number to dB and phase
        
        Parameters : zIn : Complex input (np.array[Re, Im])

        Returns: Tuple of dB and Phase (db, Phase)       
        '''
        
        try:
            return np.angle(zIn, deg)
            
            #print(np.arctan(zIn) * (180/np.pi))
            #return np.arctan(zIn) * (180/np.pi)
        except Exception as e:
            print(e)

    def s2mm(self):
        '''
        Convert single ended matrix to mixed mode:
        -------------------|---------------------
        |                  |                    |
        |                  |                    |
        |        DD        |        DC          |
        |                  |                    |
        |                  |                    |
        |------------------|--------------------| 
        |                  |                    |
        |        CD        |        CC          |
        |                  |                    |
        |                  |                    |
        -------------------|---------------------
                                     

        '''
        self.se = self.s #single ended
        self.se2gmm(p = int(self.num_ports/2))    
        self.mm = self.s #mixed mode
        halfWay = int(self.getNumPorts(self.mm)/2)
        self.dd = self.mm[:,:halfWay,:halfWay]  #diff-diff
        self.dc = self.mm[:,:halfWay,halfWay:]  #diff-comm
        self.cd = self.mm[:,halfWay:,:halfWay]  #comm-diff
        self.cc = self.mm[:,halfWay:,halfWay:]  #comm-comm

        #print self.dd[0]
        

    def getNumPorts(self, matrix):
        
        return matrix[0].shape[0]
    
    def merge_dicts(self, *dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result


    @property
    def freq_unit(self):
        return self.frequency.unit

    @freq_unit.setter
    def freq_unit(self, unit):

        unit_dict = {"hz" : 1,
                     "khz" : 2,
                     "mhz" : 3,
                     "ghz" : 4}

        current_unit = unit_dict[self.frequency.unit.lower()]
        desired_unit = unit_dict[unit.lower()]

        self.freq = self.freq * (1000 ** (current_unit - desired_unit))
        self.frequency.unit = unit

        #print("F Was: {}, F Now:{}".format(unit, self.frequency.unit))

        

            
if __name__ == "__main__":

    vna_out = SNPManipulations('snps/TestDelay.s8p')
    vna_out.one_sided = False
    
    #vna_out.renumber([1,2], [2,1])
    vna_out.renumber([0,1,2,3,4,5,6,7], [0,2,5,4,3,1,6,7])
    
    vna_out.s2mm()

    vna_out.port_name = {0:"12", 1:"36", 2:"45", 3:"78",4:"(r)12", 5:"(r)36", 6:"(r)45", 7:"(r)78"}

    vna_out.getRL(vna_out.dd, z=True)

    print("Before ",vna_out.RL_dict["12"][0])
    
    vna_out.renumber([0,2,5,4,3,1,6,7], [0,1,2,3,4,5,6,7])
    vna_out.s2mm()
    vna_out.port_name = {0:"12", 1:"36", 2:"45", 3:"78",4:"(r)12", 5:"(r)36", 6:"(r)45", 7:"(r)78"}

    #print vna_out.cc[0]

    #vna_out.write_touchstone("testout_mm", form="ri")
        
    vna_out.getRL(vna_out.dd, z=True)

    print("After ",vna_out.RL_dict["12"][0])
    #print(vna_out.RL_dict["12"][0].real)
    #print(vna_out.RL_dict["12"][0].imag)

    vna_out.freq_unit = "MHz"
    #print(vna_out.freq)

    vna_out.freq_unit = "kHz"
    #print(vna_out.freq)
    


    #vna_out.getACRF(vna_out.dd)

    #print vna_out.dd[1]

    #for (vals) in vna_out.RL_dict["36"][:1]:
    #    print(-20*np.log10(np.absolute(vals)))
    #print(vna_out.freq[1000-1])
