from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy import N, log
from sympy import Symbol
import math

class Limit:

    def __init__(self, parameter, clauses=[""], bounds=[-math.inf, math.inf]):
        self.clauses = clauses
        self.parameter = parameter
        self.parseClauses(clauses)
        self.bounds = bounds
        self.resultsDict = None
        self.resultsList = None

    def __str__(self):
        return self.clauses[0]

    def __repr__(self):
        return self.clauses[0]

    def parseClauses(self, clauses):
        transformation = standard_transformations + (implicit_multiplication_application, convert_xor)
        self.functions = []
        for clause in clauses:
            if not (clause == ""):
                self.functions.append(parse_expr(clause, local_dict={"log":lambda x: log(x, 10)}, transformations=transformation))

    def evaluate(self, vals, neg=False):
        i = 0
        for function in self.functions:
            for symbol in function.free_symbols:
                if not(symbol.__str__() in vals):
                    return 0
            if self.bounds[i] <= vals['f'] and vals['f'] <= self.bounds[i+1]:
                try:
                    if neg:
                        return -1 * N(function.subs(vals))
                    else:
                        return N(function.subs(vals), 2)
                except:
                    print(self.parameter)
            i += 1
        return 0

    def evaluateDict(self, vals, nb, neg=False):
        if not self.resultsDict:
            self.evaluatePoints(vals, nb, neg)        

        return self.resultsDict

    def evaluateArray(self, vals, nb, neg=False):
        if not self.resultsList:
            self.evaluatePoints(vals, nb, neg)

        return self.resultsList
        
    def evaluatePoints(self, vals, nb, neg=False):
        if not (self.functions is []):
            self.resultsDict = {}
            self.resultsList = []
            for i in range(0, nb):
                valsDict = {}
                for param in vals:
                    valsDict[param] = vals[param][i]
                if self.bounds[0] <= vals['f'][i] and vals['f'][i] <= self.bounds[-1]:
                    self.resultsDict[vals['f'][i]] = self.evaluate(valsDict, neg)
                    self.resultsList.append((vals['f'][i], self.resultsDict[vals['f'][i]]))
        
