from parameters.returnloss       import ReturnLoss
from parameters.next             import NEXT
from parameters.propagationdelay import PropagationDelay
from parameters.insertionloss    import InsertionLoss
from parameters.psnext           import PSNEXT
from parameters.lcl              import LCL
from parameters.tcl              import TCL
from parameters.cmrl             import CMRL
from parameters.cmnext           import CMNEXT
from parameters.cmdmnext         import CMDMNEXT
from parameters.cmdmrl           import CMDMRL
from parameters.dmcmnext         import DMCMNEXT
from parameters.dmcmrl           import DMCMRL
from parameters.tctl             import TCTL
from parameters.lctl             import LCTL
from parameters.psacrf           import PSACRF
from parameters.psfext           import PSFEXT
from parameters.acrf             import ACRF
from parameters.eltctl           import ELTCTL
from parameters.fext             import FEXT
from parameters.axext            import ANEXT, AFEXT
from parameters.psaxext          import PSANEXT, PSAFEXT
from parameters.psaacrx          import PSAACRX, PSAACRN, PSAACRF
from parameters.dfdelay          import DFDelay
from parameters.plugdelay        import PlugDelay
from parameters.nextdelay        import NEXTDelay
from parameters.correctednext    import CorrectedNEXT
from parameters.dnext            import DNEXT
from parameters.case             import Case

class ParameterFactory(object):
    def __init__(self, config, freq, matrices, parameters):
        self._config   = config
        self._freq     = freq
        self._matrices = matrices

        self._computed = dict()
        self._computed.update(parameters)
        self._factory = self.setUpFactory(config, freq, matrices)

    def setUpFactory(self, c, f, m):
        parameters = {
            ACRF, ANEXT, AFEXT, Case, CMDMNEXT, DMCMRL, CMNEXT, CMRL,
            CorrectedNEXT, DFDelay, DMCMNEXT, DMCMRL, DNEXT, ELTCTL,
            FEXT, LCL, LCTL, NEXTDelay, NEXT, PlugDelay, PropagationDelay,
            PSAACRX, PSAACRN, PSAACRF, PSACRF, PSANEXT, PSAFEXT, PSFEXT,
            PSNEXT, ReturnLoss,
        }
        return {cls.getType() : cls.register(self.getParameter) for cls in parameters}

    def getParameter(self, name):
        # compute the parameter if it wasn't computed
        if name not in self._computed.keys():
            self._computed[name] = self._factory[name](self._config, self._freq, self._matrices)

        # return the computed parameter
        return self._computed[name]
