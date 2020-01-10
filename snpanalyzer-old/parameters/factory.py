from snpanalyzer.parameters.returnloss       import ReturnLoss
from snpanalyzer.parameters.next             import NEXT
from snpanalyzer.parameters.propagationdelay import PropagationDelay
from snpanalyzer.parameters.insertionloss    import InsertionLoss
from snpanalyzer.parameters.psnext           import PSNEXT
from snpanalyzer.parameters.lcl              import LCL
from snpanalyzer.parameters.tcl              import TCL
from snpanalyzer.parameters.cmrl             import CMRL
from snpanalyzer.parameters.cmnext           import CMNEXT
from snpanalyzer.parameters.cmdmnext         import CMDMNEXT
from snpanalyzer.parameters.cmdmrl           import CMDMRL
from snpanalyzer.parameters.dmcmnext         import DMCMNEXT
from snpanalyzer.parameters.dmcmrl           import DMCMRL
from snpanalyzer.parameters.tctl             import TCTL
from snpanalyzer.parameters.lctl             import LCTL
from snpanalyzer.parameters.psacrf           import PSACRF
from snpanalyzer.parameters.psfext           import PSFEXT
from snpanalyzer.parameters.acrf             import ACRF
from snpanalyzer.parameters.eltctl           import ELTCTL
from snpanalyzer.parameters.fext             import FEXT
from snpanalyzer.parameters.axext            import ANEXT, AFEXT
from snpanalyzer.parameters.psaxext          import PSANEXT, PSAFEXT
from snpanalyzer.parameters.psaacrx          import PSAACRX, PSAACRN, PSAACRF
from snpanalyzer.parameters.dfdelay          import DFDelay
from snpanalyzer.parameters.plugdelay        import PlugDelay, JackDelay
from snpanalyzer.parameters.nextdelay        import NEXTDelay, JackNEXTDelay
from snpanalyzer.parameters.correctednext    import CorrectedNEXT
from snpanalyzer.parameters.dnext            import DNEXT, ReverseDNEXT
from snpanalyzer.parameters.case             import Case, ReverseCase

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
            PSAACRN, PSAACRF, PSACRF, PSANEXT, PSAFEXT, PSFEXT,
            PSNEXT, ReturnLoss, InsertionLoss, CMDMRL, TCTL, TCL, JackDelay,
            JackNEXTDelay, ReverseDNEXT, ReverseCase
        }
        return {cls.getType() : cls.register(self.getParameter) for cls in parameters}

    def getParameter(self, name):
        # compute the parameter if it wasn't computed
        if name not in self._computed.keys():
            self._computed[name] = self._factory[name](self._config, self._freq, self._matrices)

        # return the computed parameter
        return self._computed[name]
