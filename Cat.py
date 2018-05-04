class cat6A(objet):

    def __init__(self, hardware):

        #Connecting Hardware
        self.minFreq = 1    #MHz
        self.maxFreq = 500  #MHz
        
        self.RL       = lambda f: np.piecewise(f, [(f > minFreq) * (f < 79), (f >=79)*(f <= maxFreq)], [30, lambda f: 28.0 - 20.0 * np.log10(f/100)])
        self.IL       = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 0.02 * np.sqrt(f)])
        self.NEXT     = lambda f: np.piecewise(f, [(f > minFreq) * (f < 250), (f >= 250)*(f <= maxFreq)], [lambda f: 54 - 20*np.log10(f/100) , 46.04 - 40 * np.log10(f/250)])
        self.PSNEXT   = lambda f: np.piecewise(f, [(f > minFreq) * (f < 250), (f >= 250)*(f <= maxFreq)], [lambda f: 50 - 20*np.log10(f/100) , 42.04 - 40 * np.log10(f/250)])
        self.FEXT     = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 43.1-20*np.log(f/100)])
        self.PSFEXT   = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 40.1-20*np.log(f/100)])
        self.TCL      = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 28 - 20*np.log(f/100)])
        self.TCTL     = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 28-20*np.log(f/100)])

class cat6(objet):

    def __init__(self, hardware):
        #Connecting Hardware
        self.minFreq = 1    #MHz
        self.maxFreq = 500  #MHz
        
        self.RL       = lambda f: np.piecewise(f, [(f > minFreq) * (f < 79), (f >=79)*(f <= maxFreq)], [30, lambda f: 28.0 - 20.0 * np.log10(f/100)])
        self.IL       = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 0.02 * np.sqrt(f)])
        self.NEXT     = lambda f: np.piecewise(f, [(f > minFreq) * (f < 250), (f >= 250)*(f <= maxFreq)], [lambda f: 54 - 20*np.log10(f/100) , 46.04 - 40 * np.log10(f/250)])
        self.PSNEXT   = lambda f: np.piecewise(f, [(f > minFreq) * (f < 250), (f >= 250)*(f <= maxFreq)], [lambda f: 50 - 20*np.log10(f/100) , 42.04 - 40 * np.log10(f/250)])
        self.FEXT     = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 43.1-20*np.log(f/100)])
        self.PSFEXT   = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 40.1-20*np.log(f/100)])
        self.TCL      = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 28 - 20*np.log(f/100)])
        self.TCTL     = lambda f: np.piecewise(f, [(f > minFreq) * (f < maxFreq)], [lambda f: 28-20*np.log(f/100)])
