import configparser

class Settings:

    def __init__(self):
        
        self.settings_file = 'SETTINGS.ini'

        self.config = configparser.ConfigParser()
        self.config.read_file(open(self.settings_file))
        

    @property
    def pairNames(self):
        try:
            names = []
            for key,val in self.config['pair_names'].items():
                names.append(val)
            return names
        except Exception as e:
            return []

    @pairNames.setter
    def pairNames(self, names  : list):
        print("Saving Pair Names")
        print(names)
        self.config['pair_names'] = {}
        if len(names) != len(set(names)):
            raise Exception("Ports must contain unique names")
        for i, name in enumerate(names):
            self.config['pair_names']["PAIR_"+str(i+1)] = name 
            
            with open(self.settings_file, 'w') as configfile:
                self.config.write(configfile)


    @property
    def pairNamesAlien(self):
        try:
            names = []
            for key,val in self.config['alien_pair_names'].items():
                names.append(val)
            return names
        except Exception as e:
            return []

    @pairNamesAlien.setter
    def pairNamesAlien(self, names  : list):
        print("Saving Alien Pair Names")
        print(names)
        self.config['alien_pair_names'] = {}
        if len(names) != len(set(names)):
            raise Exception("Ports must contain unique names")
        for i, name in enumerate(names):
            self.config['alien_pair_names']["PAIR_"+str(i+1)] = name 
            
            with open(self.settings_file, 'w') as configfile:
                self.config.write(configfile)


    @property
    def numPairs(self):
        return int(self.config['PXI']['num_pairs'])


    @numPairs.setter
    def numPairs(self, num_pairs  : int):
        self.config['PXI']['num_pairs'] = str(num_pairs)