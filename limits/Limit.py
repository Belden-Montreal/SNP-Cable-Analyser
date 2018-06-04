from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy import N
from sympy import Symbol, refine, Q
import math

class Limit:

    def __init__(self, parameter, clauses=[""], bounds=[-math.inf, math.inf]):
        self.clauses = clauses
        self.parameter = parameter
        self.parseClauses(clauses)
        self.bounds = bounds

    def __str__(self):
        return self.clauses[0]

    def __repr__(self):
        return self.clauses[0]

    def parseClauses(self, clauses):
        transformation = standard_transformations + (implicit_multiplication_application, convert_xor)
        self.functions = []
        for clause in clauses:
            if not (clause == ""):
                self.functions.append(refine(parse_expr(clause, transformations=transformation)))

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
                        return N(function.subs(vals))
                except:
                    print(self.parameter)
            i += 1
        return 0

    def evaluateDict(self, vals, nb, neg=False):
        results = {}
        if not (self.functions is []):
            for i in range(0, nb):
                valsDict = {}
                for param in vals:
                    valsDict[param] = vals[param][i]
                if self.bounds[0] <= vals['f'][i] and vals['f'][i] <= self.bounds[-1]:
                    results[vals['f'][i]] = self.evaluate(valsDict, neg)
        return results

    def evaluateArray(self, vals, nb, neg=False):
        results = []
        if not (self.functions is []):
            for i in range(0, nb):
                valsDict = {}
                for param in vals:
                    valsDict[param] = vals[param][i]
                if self.bounds[0] <= vals['f'][i] and vals['f'][i] <= self.bounds[-1]:
                    results.append((vals['f'][i], self.evaluate(valsDict, neg)))
        return results
        
        
