from parameters.parameter import PairedParameter

class NEXTDelay(PairedParameter):

    def __init__(self, ports, freq, matrices, plugDelay):
        self._plugDelay = plugDelay
        super(NEXTDelay, self).__init__(ports, freq, matrices)

    def computePairs(self, ports):
        # create each pair for the NEXT
        pairs = dict()
        for i in range(0, len(ports)//2):
            for j in range(0, len(ports)//2):
                if i >= j:
                    continue

                # create the pair for the first end of the line
                port1 = i
                port2 = j
                pairs[(port1, port2)] = ports[port1]+"-"+ports[port2]
                pairs[(port2, port1)] = ports[port2]+"-"+ports[port1]

                # create the pair for the second end of the line
                port1 = i + len(ports)//2
                port2 = j + len(ports)//2
                pairs[(port1, port2)] = ports[port1]+"-"+ports[port2]
                pairs[(port2, port1)] = ports[port2]+"-"+ports[port1]

        return pairs

    def computeParameter(self):
        nextDelay = dict()
        plugDelay = self._plugDelay.getParameter()

        for i in plugDelay:
            for j in range(i+1, len(plugDelay)):
                nextDelay[(i,j)] = plugDelay[i] + plugDelay[j]

        return nextDelay,None

    def getPlugDelay(self):
        return self._plugDelay

    def getName(self):
        return "NEXTDelay"

    def chooseMatrices(self, matrices):
        return None