from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy import N, log, E
from sympy import Symbol
import math
from multiprocessing.dummy import Pool as ThreadPool
class Limit:

    def __init__(self, parameter, clauses=[""], bounds=[-math.inf, math.inf], maxValue=math.inf):
        self.clauses = clauses
        self.maxValue = maxValue
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
                self.functions.append(parse_expr(clause, local_dict={"log":lambda x: log(x, 10), "e": E}, transformations=transformation))

    def evaluate(self, vals):
        for i, function in enumerate(self.functions):
            for symbol in function.free_symbols:
                if not(symbol.__str__() in vals):
                    return 0
            if self.bounds[i] <= vals['f'] and vals['f'] <= self.bounds[i+1]:
                try:
                    val = N(function.subs(vals))
                    if val > self.maxValue:
                        val = self.maxValue
                    return val
                except:
                    print("Eval error")
        return 0

    def evaluateDict(self, vals, nb, neg=False):
        if not len(self.functions):
            return
        if not self.resultsDict:
            self.evaluatePoints(vals, nb)        
        if neg:
            return {x: -self.resultsDict[x] for x in self.resultsDict.keys()}
        return self.resultsDict

    def evaluateArray(self, vals, nb, neg=False):
        if not len(self.functions):
            return
        if not self.resultsList:
            self.evaluatePoints(vals, nb)
        if neg:
            return [(x,-y) for x,y in self.resultsList]
        return self.resultsList
        
    def evaluatePoints(self, vals, nb):
        if not (self.functions is []):
            self.resultsDict = {}
            self.resultsList = []
            for i in range(0, nb):
                valsDict = {}
                for param in vals:
                    valsDict[param] = vals[param][i]
                if self.bounds[0] <= vals['f'][i] and vals['f'][i] <= self.bounds[-1]:
                    self.resultsDict[vals['f'][i]] = self.evaluate(valsDict)
                    self.resultsList.append((vals['f'][i], self.resultsDict[vals['f'][i]]))
            # valsList = [] #MULTITHREADING
            # for i in range(0,nb):
            #     valsDict = {}
            #     for param in vals:
            #         valsDict[param] = vals[param][i]
            #     valsList.append(valsDict)
            # pool = ThreadPool()
            # results = pool.starmap(self.evaluatePoint, zip(valsList, [neg]*nb))
            # self.resultsList = [x for x in results if x is not None]
            # for res in self.resultsList:
            #     if res:
            #         self.resultsDict[res[0]] = res[1]
        
    # def evaluatePoint(self, valsDict, neg):
    #     if self.bounds[0] <= valsDict['f'] and valsDict['f'] <= self.bounds[-1]:
    #         return (valsDict['f'], self.evaluate(valsDict, neg))

    def setParamValue(self, symbol, value):
        for i, function in enumerate(self.functions):
            if symbol in function.free_symbols:
                self.functions[i] = function.subs(symbol, value)
                print(str(self.functions[i]))