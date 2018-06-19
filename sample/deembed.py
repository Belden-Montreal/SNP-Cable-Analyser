from sample.sample import Sample

class Deembed(Sample):

    def __init__(self, matedLoad, plugNext, plugNextDelay):
        self._plugNext = plugNext
        self._plugNextDelay = plugNextDelay
        super(Deembed, self).__init__(matedLoad)

    def addParameters(self):
        parameters = [
            "PCNEXT",
            "NEXTDelay",
            "DNEXT",
        ]

        for parameter in parameters:
            if parameter == "PCNEXT":
                self._parameters[parameter] = self._plugNext
            elif parameter == "NEXTDelay":
                self._parameters[parameter] = self._plugNextDelay
            else:
                self._parameters[parameter] = self._factory.getParameter(parameter)