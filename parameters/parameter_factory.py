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
from parameters.axext            import AXEXT
from parameters.psaxext          import PSAXEXT
from parameters.psaacrx          import PSAACRX
from parameters.dfdelay          import DFDelay
from parameters.plugdelay        import PlugDelay
from parameters.nextdelay        import NEXTDelay
from parameters.correctednext    import CorrectedNEXT
from parameters.dnext            import DNEXT
from parameters.case             import Case

class ParameterFactory(object):
    def __init__(self, config, freq, matrices, parameters):
        self._parameters = parameters
        self._factory = self.setUpFactory(config, freq, matrices)

    def setUpFactory(self, c, f, m):
        p = lambda param: self.getParameter(param)
        return {
            "RL"               :lambda:       ReturnLoss(c, f, m),
            "IL"               :lambda:    InsertionLoss(c, f, m),
            "NEXT"             :lambda:             NEXT(c, f, m),
            "PSNEXT"           :lambda:           PSNEXT(c, f, m, p("NEXT")),
            "Propagation Delay":lambda: PropagationDelay(c, f, m, p("RL")),
            "FEXT"             :lambda:             FEXT(c, f, m),
            "PSFEXT"           :lambda:           PSFEXT(c, f, m, p("FEXT")),
            "ACRF"             :lambda:             ACRF(c, f, m, p("FEXT"), p("IL")),
            "PSACRF"           :lambda:           PSACRF(c, f, m, p("PSFEXT"), p("IL")),
            "LCL"              :lambda:              LCL(c, f, m),
            "LCTL"             :lambda:             LCTL(c, f, m),
            "TCL"              :lambda:              TCL(c, f, m),
            "TCTL"             :lambda:             TCTL(c, f, m),
            "ELTCTL"           :lambda:           ELTCTL(c, f, m, p("IL"), p("TCTL")),
            "CMRL"             :lambda:             CMRL(c, f, m),
            "CMNEXT"           :lambda:           CMNEXT(c, f, m),
            "CMDMNEXT"         :lambda:         CMDMNEXT(c, f, m),
            "CMDMRL"           :lambda:           CMDMRL(c, f, m),
            "DMCMNEXT"         :lambda:         DMCMNEXT(c, f, m),
            "DMCMRL"           :lambda:           DMCMRL(c, f, m),
            "ANEXT"            :lambda:            AXEXT(c, f, m, p("FEXT"), p("IL")),
            "AFEXT"            :lambda:            AXEXT(c, f, m, p("FEXT"), p("IL")),
            "PSANEXT"          :lambda:          PSAXEXT(c, f, m, p("ANEXTD")),
            "PSAACRN"          :lambda:          PSAACRX(c, f, m, p("PSANEXT"), p("IL")),
            "PSAFEXT"          :lambda:          PSAXEXT(c, f, m, p("AFEXTD")),
            "PSAACRX"          :lambda:          PSAACRX(c, f, m, p("PSAXEXT"), p("IL")),
            "DFDelay"          :lambda:          DFDelay(c, f, m, p("DFOpenDelay"), p("DFShortDelay")),
            "NEXTDelay"        :lambda:        NEXTDelay(c, f, m, p("PlugDelay")),
            "CNEXT"            :lambda:    CorrectedNEXT(c, f, m, p("NEXTDelay")),
            "DNEXT"            :lambda:            DNEXT(c, f, m, p("NEXTDelay"), p("PCNEXT")),
            "Case"             :lambda:             Case(c, f, m, p("DNEXT"), p[" PCNEXT"], p("Cases")),
            "PlugDelay"        :lambda:        PlugDelay(c, f, m, p("PlugOpenDelay"), p("PlugShortDelay"),
                                                                  p("DFDelay"), p("k1"),
                                                                  p("k2"), p("k3")),
        }

    def getParameter(self, name):
        if name not in self._parameters.keys():
            self._parameters[name] = self._factory[name]()
        return self._parameters[name]
