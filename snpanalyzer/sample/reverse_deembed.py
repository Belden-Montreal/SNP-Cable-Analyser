from snpanalyzer.sample.single_ended import SingleEnded

class ReverseDeembed(SingleEnded):

    def __init__(self, matedLoad, plugDelay, plugNext, openDelay, shortDelay, k1, k2, k3, cases):
        self._plugNext = plugNext
        self._plugDelay = plugDelay
        self._openDelay = openDelay
        self._shortDelay = shortDelay
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        self._cases = cases
        super(ReverseDeembed, self).__init__(matedLoad)

    def addParameters(self):
        parameters = [
            "RL",
            "NEXT",
            "PCNEXT",
            "k1",
            "k2",
            "k3",
            "PlugDelay",
            "OpenDelay",
            "ShortDelay",
            "JackDelay",
            "JackNEXTDelay",
            "RDNEXT",
            "Cases",
            "RCase",
        ]

        for parameter in parameters:
            if parameter == "PCNEXT":
                self._parameters[parameter] = self._plugNext
            elif parameter == "OpenDelay":
                self._parameters[parameter] = self._openDelay
            elif parameter == "ShortDelay":
                self._parameters[parameter] = self._shortDelay
            elif parameter == "PlugDelay":
                self._parameters[parameter] = self._plugDelay
            elif parameter == "Cases":
                self._parameters[parameter] = self._cases
            elif parameter == "k1":
                self._parameters[parameter] = self._k1
            elif parameter == "k2":
                self._parameters[parameter] = self._k2
            elif parameter == "k3":
                self._parameters[parameter] = self._k3
            else:
                self._parameters[parameter] = self._factory.getParameter(parameter)