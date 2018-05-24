from sympy.parsing import sympy_parser

class Limit:

    def __init__(self, clause):
        self.clause = clause
        self.function = self.parseClause(clause)

    def __str__(self):
        return self.clause

    def __repr__(self):
        return self.clause

    def parseClause(self, clause):
        return sympy_parser.parse_expr(clause)

    def evaluateLimit(self):
        return self.function()