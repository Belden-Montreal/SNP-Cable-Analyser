from parameters.parameter import Parameter, complex2db

class Fext(Parameter):
    def computeParameter(self):
        fext = dict()
        cpFext = dict()
        for i,porti in sorted(self._ports.items())[len(self._ports)//2:]:
            for j,portj in sorted(self._ports.items())[:len(self._ports)//2]:
                if not (i == j) and not (abs(i-j) == len(self._ports)//2):
                    fext[porti+"-"+portj] = list()
                    fext[portj+"-"+porti] = list()
                    cpFext[porti+"-"+portj] = list()
                    cpFext[portj+"-"+porti] = list()

        # extract the fext in all matrices
        for (f,_) in enumerate(self._freq):
            for i,porti in sorted(self._ports.items())[len(self._ports)//2:]:
                for j,portj in sorted(self._ports.items())[:len(self._ports)//2]:
                    # get the value
                    if not (i == j) and not (abs(i-j) == len(self._ports)//2):
                        topRight = self._matrices[f, i, j]
                        bottomLeft = self._matrices[f, j, i]
                        fext[porti+"-"+portj].append(complex2db(bottomLeft))
                        fext[portj+"-"+porti].append(complex2db(topRight))
                        cpFext[porti+"-"+portj].append(bottomLeft)
                        cpFext[portj+"-"+porti].append(topRight)

        return fext, cpFext