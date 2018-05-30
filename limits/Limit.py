from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from sympy import N
class Limit:

    def __init__(self, parameter, clause):
        self.clause = clause
        self.parameter = parameter
        self.function = self.parseClause(clause)

    def __str__(self):
        return self.clause

    def __repr__(self):
        return self.clause

    def parseClause(self, clause):
        transformation = standard_transformations + (implicit_multiplication_application, convert_xor)
        return parse_expr(clause, transformations=transformation)

    def evaluate(self, vals):
        for symbol in self.function.free_symbols:
            if not(symbol.__str__() in vals):
                return "Error. Parameter "+symbol.__str__()+" not provided"
        return N(self.function.subs(vals))