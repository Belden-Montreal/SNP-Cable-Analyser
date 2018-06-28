from sample.single_ended import SingleEnded

class Deembed(SingleEnded):

    def __init__(self, matedLoad, plugNext, plugNextDelay, cases):
        self._plugNext = plugNext
        self._plugNextDelay = plugNextDelay
        self._cases = cases
        super(Deembed, self).__init__(matedLoad)

    def addParameters(self):
        parameters = [
            "PCNEXT",
            "NEXTDelay",
            "DNEXT",
            "Cases",
            "Case",
        ]

        for parameter in parameters:
            if parameter == "PCNEXT":
                self._parameters[parameter] = self._plugNext
            elif parameter == "NEXTDelay":
                self._parameters[parameter] = self._plugNextDelay
            elif parameter == "Cases":
                self._parameters[parameter] = self._cases
            else:
                self._parameters[parameter] = self._factory.getParameter(parameter)