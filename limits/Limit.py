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
        self.negResultsDict = None
        self.resultsList = None
        self.negResultsList = None

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

    def evaluate(self, vals):
        for i, function in enumerate(self.functions):
            for symbol in function.free_symbols:
                if not(symbol.__str__() in vals):
                    return (0,0)
            if self.bounds[i] <= vals['f'] and vals['f'] <= self.bounds[i+1]:
                try:
                    val = N(function.subs(vals))
                    return val, -1*val
                except:
                    print("Eval error")
        return (0,0)

    def evaluateDict(self, vals, nb, neg=False):
        if not self.resultsDict:
            self.evaluatePoints(vals, nb)        

        if neg:
            return self.negResultsDict
        return self.resultsDict

    def evaluateArray(self, vals, nb, neg=False):
        if not self.resultsList:
            self.evaluatePoints(vals, nb)

        if neg:
            return self.negResultsList
        return self.resultsList
        
    def evaluatePoints(self, vals, nb):
        if not (self.functions is []):
            self.resultsDict = {}
            self.negResultsDict = {}
            self.resultsList = []
            self.negResultsList = []
            for i in range(0, nb):
                valsDict = {}
                for param in vals:
                    valsDict[param] = vals[param][i]
                if self.bounds[0] <= vals['f'][i] and vals['f'][i] <= self.bounds[-1]:
                    val, negVal = self.evaluate(valsDict)
                    self.resultsDict[vals['f'][i]] = val
                    self.resultsList.append((vals['f'][i], val))
                    self.negResultsDict[vals['f'][i]] = negVal
                    self.negResultsList.append((vals['f'][i], negVal))
        
