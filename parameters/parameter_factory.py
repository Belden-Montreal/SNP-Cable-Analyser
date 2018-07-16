from parameters.returnloss import ReturnLoss
from parameters.next import NEXT
from parameters.propagationdelay import PropagationDelay
from parameters.insertionloss import InsertionLoss
from parameters.psnext import PSNEXT
from parameters.lcl import LCL
from parameters.tcl import TCL
from parameters.cmrl import CMRL
from parameters.cmnext import CMNEXT
from parameters.cmdmnext import CMDMNEXT
from parameters.cmdmrl import CMDMRL
from parameters.dmcmnext import DMCMNEXT
from parameters.dmcmrl import DMCMRL
from parameters.tctl import TCTL
from parameters.lctl import LCTL
from parameters.psacrf import PSACRF
from parameters.psfext import PSFEXT
from parameters.acrf import ACRF
from parameters.eltctl import ELTCTL
from parameters.fext import FEXT
from parameters.axext import AXEXT
from parameters.psaxext import PSAXEXT
from parameters.psaacrx import PSAACRX
from parameters.dfdelay import DFDelay
from parameters.plugdelay import PlugDelay
from parameters.nextdelay import NEXTDelay
from parameters.correctednext import CorrectedNEXT
from parameters.dnext import DNEXT
from parameters.case import Case

class ParameterFactory(object):

    def __init__(self, ports, freq, matrix, params):
        self._ports = ports
        self._freq = freq
        self._matrix = matrix
        self._params = params
        self.__parameters = {
            "RL":lambda: ReturnLoss(self._ports, self._freq, self._matrix),
            "IL":lambda: InsertionLoss(self._ports, self._freq, self._matrix),
            "NEXT":lambda: NEXT(self._ports, self._freq, self._matrix),
            "PSNEXT":lambda: PSNEXT(self._ports, self._freq, self._matrix, self._params["NEXT"]),
            "Propagation Delay":lambda: PropagationDelay(self._ports, self._freq, self._matrix, self._params["RL"]),
            "FEXT":lambda: FEXT(self._ports, self._freq, self._matrix),
            "PSFEXT":lambda: PSFEXT(self._ports, self._freq, self._matrix, self._params["FEXT"]),
            "ACRF":lambda: ACRF(self._ports, self._freq, self._matrix, self._params["FEXT"], self._params["IL"]),
            "PSACRF":lambda: PSACRF(self._ports, self._freq, self._matrix, self._params["PSFEXT"], self._params["IL"]),
            "LCL":lambda: LCL(self._ports, self._freq, self._matrix),
            "LCTL":lambda: LCTL(self._ports, self._freq, self._matrix),
            "TCL":lambda: TCL(self._ports, self._freq, self._matrix),
            "TCTL":lambda: TCTL(self._ports, self._freq, self._matrix),
            "ELTCTL":lambda: ELTCTL(self._ports, self._freq, self._matrix, self._params["IL"], self._params["TCTL"]),
            "CMRL":lambda: CMRL(self._ports, self._freq, self._matrix),
            "CMNEXT":lambda: CMNEXT(self._ports, self._freq, self._matrix),
            "CMDMNEXT":lambda: CMDMNEXT(self._ports, self._freq, self._matrix),
            "CMDMRL":lambda: CMDMRL(self._ports, self._freq, self._matrix),
            "DMCMNEXT":lambda: DMCMNEXT(self._ports, self._freq, self._matrix),
            "DMCMRL":lambda: DMCMRL(self._ports, self._freq, self._matrix),
            "ANEXT":lambda: AXEXT(self._ports, self._freq, self._matrix, self._params["FEXT"], self._params["IL"]),
            "AFEXT":lambda: AXEXT(self._ports, self._freq, self._matrix, self._params["FEXT"], self._params["IL"]),
            "PSANEXT":lambda: PSAXEXT(self._ports, self._freq, self._matrix, self._params["ANEXTD"]),
            "PSAACRN":lambda: PSAACRX(self._ports, self._freq, self._matrix, self._params["PSANEXT"], self._params["IL"]),
            "PSAFEXT":lambda: PSAXEXT(self._ports, self._freq, self._matrix, self._params["AFEXTD"]),
            "PSAACRF":lambda: PSAACRX(self._ports, self._freq, self._matrix, self._params["PSAFEXT"], self._params["IL"]),
            "DFDelay":lambda: DFDelay(self._ports, self._freq, self._matrix, self._params["DFOpenDelay"], self._params["DFShortDelay"]),
            "PlugDelay":lambda: PlugDelay(self._ports, self._freq, self._matrix, self._params["PlugOpenDelay"], self._params["PlugShortDelay"], self._params["DFDelay"], self._params["k1"], self._params["k2"], self._params["k3"]),
            "NEXTDelay":lambda: NEXTDelay(self._ports, self._freq, self._matrix, self._params["PlugDelay"]),
            "CNEXT":lambda: CorrectedNEXT(self._ports, self._freq, self._matrix, self._params["NEXTDelay"]),
            "DNEXT":lambda: DNEXT(self._ports, self._freq, self._matrix, self._params["NEXTDelay"], self._params["PCNEXT"]),
            "Case":lambda: Case(self._ports, self._freq, self._matrix, self._params["DNEXT"], self._params["PCNEXT"], self._params["Cases"]),
        }

    def getParameter(self, name):
        return self.__parameters[name]()
