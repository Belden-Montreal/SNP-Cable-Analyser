from sample.sample import Sample

class Delay(Sample):

    def addParameters(self):
        parameters = [
            "RL",
            "Propagation Delay",
        ]

        for parameter in parameters:
            self._parameters[parameter] = self._factory.getParameter(parameter)