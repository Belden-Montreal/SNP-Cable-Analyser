from parameters.parameter import PairedParameter

class NEXTDelay(PairedParameter):

    def __init__(self, ports, freq, matrices, plugDelay):
        self._plugDelay = plugDelay
        super(NEXTDelay, self).__init__(ports, freq, matrices)
        self._visible = False

    def computePairs(self, ports):
        # create each pair for the NEXT
        pairs = dict()
        for i in range(0, len(ports)//2):
            for j in range(0, len(ports)//2):
                if i >= j:
                    continue

                # create the pair for the first end of the line
                port1,isRemote1 = ports[i]
                port2,isRemote2 = ports[j]
                pairs[(i, j)] = (port1+"-"+port2, isRemote1)
                pairs[(j, i)] = (port2+"-"+port1, isRemote2)

                # create the pair for the second end of the line
                port1,isRemote1 = ports[i + len(ports)//2]
                port2,isRemote2 = ports[j + len(ports)//2]
                pairs[(i+ len(ports)//2, j+ len(ports)//2)] = (port1+"-"+port2, isRemote1)
                pairs[(j+ len(ports)//2, i+ len(ports)//2)] = (port2+"-"+port1, isRemote2)

        return pairs

    def computeParameter(self):
        nextDelay = dict()
        plugDelay = self._plugDelay.getParameter()

        for (i,j) in plugDelay:
            for k in range(i+1, len(plugDelay)):
                nextDelay[(i,k)] = plugDelay[(i,j)] + plugDelay[(k,k)]

        return nextDelay,None
    
    def recalculate(self, plugDelay):
        self._plugDelay = plugDelay
        (self._parameter, self._complexParameter) = self.computeParameter()

    def getPlugDelay(self):
        return self._plugDelay

    def getName(self):
        return "NEXTDelay"

    def chooseMatrices(self, matrices):
        return None