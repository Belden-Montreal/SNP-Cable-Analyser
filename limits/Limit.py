from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy import N
from sympy import Symbol

class Limit:

    def __init__(self, parameter, clauses, bounds=[float('-inf'), float('inf')]):
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
            self.functions.append(parse_expr(clause, transformations=transformation))

    def evaluate(self, vals):
        i = 0
        for function in self.functions:
            for symbol in function.free_symbols:
                if not(symbol.__str__() in vals):
                    return "Error. Parameter "+symbol.__str__()+" not provided"
            if self.bounds[i] < vals['f'] and vals['f'] < self.bounds[i+1]:
                return N(function.subs(vals))
            i += 1
        return "Error. Frequency out of bounds"