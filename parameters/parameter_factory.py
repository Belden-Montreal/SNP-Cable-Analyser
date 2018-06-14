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

parameters = {
    "RL":lambda ports, freq, matrix, params: ReturnLoss(ports, freq, matrix),
    "IL":lambda ports, freq, matrix, params: InsertionLoss(ports, freq, matrix),
    "NEXT":lambda ports, freq, matrix, params: NEXT(ports, freq, matrix),
    "PSNEXT":lambda ports, freq, matrix, params: PSNEXT(ports, freq, matrix, params["NEXT"]),
    "Propagation Delay":lambda ports, freq, matrix, params: PropagationDelay(ports, freq, matrix, params["RL"]),
    "FEXT":lambda ports, freq, matrix, params: FEXT(ports, freq, matrix),
    "PSFEXT":lambda ports, freq, matrix, params: PSFEXT(ports, freq, matrix, params["FEXT"]),
    "ACRF":lambda ports, freq, matrix, params: ACRF(ports, freq, matrix, params["FEXT"], params["IL"]),
    "PSACRF":lambda ports, freq, matrix, params: PSACRF(ports, freq, matrix, params["PSFEXT"], params["IL"]),
    "LCL":lambda ports, freq, matrix, params: LCL(ports, freq, matrix),
    "LCTL":lambda ports, freq, matrix, params: LCTL(ports, freq, matrix),
    "TCL":lambda ports, freq, matrix, params: TCL(ports, freq, matrix),
    "TCTL":lambda ports, freq, matrix, params: TCTL(ports, freq, matrix),
    "ELTCTL":lambda ports, freq, matrix, params: ELTCTL(ports, freq, matrix, params["IL"], params["TCTL"]),
    "CMRL":lambda ports, freq, matrix, params: CMRL(ports, freq, matrix),
    "CMNEXT":lambda ports, freq, matrix, params: CMNEXT(ports, freq, matrix),
    "CMDMNEXT":lambda ports, freq, matrix, params: CMDMNEXT(ports, freq, matrix),
    "CMDMRL":lambda ports, freq, matrix, params: CMDMRL(ports, freq, matrix),
    "DMCMNEXT":lambda ports, freq, matrix, params: DMCMNEXT(ports, freq, matrix),
    "DMCMRL":lambda ports, freq, matrix, params: DMCMRL(ports, freq, matrix),
}
class ParameterFactory(object):

    def getParameter(self, name, ports, freq, matrix, params):
        return parameters[name](ports, freq, matrix, params)
