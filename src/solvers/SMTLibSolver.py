'''
Created on May 31, 2014

@author: ezulkosk
'''
from common.Options import standard_print
from solvers.BaseSolver import BaseSolver
import sys
class SMTLibSolver(BaseSolver):
    def __init__(self):
        self.converter = SMTLibConverter()
        self.constraints = []
        
    def setOptions(self):
        pass
        
    def add(self, constraint):
        self.constraints.append(constraint.convert(self.converter))

    def assertions(self):
        return self.constraints
    
    def printConstraints(self):
        standard_print(self.converter.parens("set-info", ":status", "unknown"))
        for i in self.converter.variables:
            standard_print(i)
        for i in self.constraints:
            standard_print(self.converter.parens("assert", i))
        standard_print(self.converter.parens("check-sat"))
        standard_print(self.converter.parens("get-model"))

class SMTLibConverter():
    
    def __init__(self):
        self.variables = []

    def parens(self, *args):
        strs = [str(i) for i in args]
        return "(" + " ".join(strs) + ")"
    
    def vardecl(self, uid, kind):
        return self.parens("declare-fun", uid, "()", kind)

    def eq_expr(self, expr):
        return self.parens("=", expr.left.convert(self), expr.right.convert(self))

    def ne_expr(self, expr):
        return self.parens("not", self.parens("=", expr.left.convert(self), expr.right.convert(self)))

    def if_expr(self, expr):
        b = expr.bool_expr.convert(self)
        t = expr.true_expr.convert(self)
        f = expr.false_expr.convert(self)
        return self.parens("ite",b,t,f)

    def implies_expr(self, expr):
        if expr.unsat_core_implies:
            #left is already converted
            l = expr.left
        else:
            l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("=>",l,r)
    
    def le_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("<=",l,r)
    
    def lt_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("<",l,r)
    
    def ge_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens(">=",l,r)
    
    def gt_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens(">",l,r)
    
    def xor_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("and",self.parens("=>",l,r),self.parens("=>",r,l))
    
    def and_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return self.parens("and", *newList)

    def or_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return self.parens("or", *newList)
    
    def sum_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        currSum = newList[0]
        for i in range(1, len(newList)):
            currSum = self.parens("+", currSum, newList[i])
        return currSum

    def plus_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("+",l,r)

    def minus_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("-",l,r)

    def times_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return self.parens("*",l,r)
    
    def divide_expr(self, expr):
        sys.exit("TODO: smtlib solver divide expr look at Z3.py")
        return None
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l / r

    def intdivide_expr(self, expr):
        sys.exit("TODO: smtlib solver intdivide expr look at Z3.py")
        return None
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l // r

    def neg_expr(self, expr):
        val = expr.value.convert(self)
        return self.parens("-",val)
    
    def not_expr(self, expr):
        val = expr.value.convert(self)
        return self.parens("not", val)

    def int_var(self, expr):
        if not expr.var:
            self.variables.append(self.vardecl(expr.id, "Int"))
            expr.var = True
        return expr.id   
    
    def real_var(self, expr):
        if not expr.var:
            self.variables.append(self.vardecl(expr.id, "Real"))
            expr.var = True
        return expr.id
    
    def bool_var(self, expr):
        if not expr.var:
            self.variables.append(self.vardecl(expr.id, "Bool"))
            expr.var = True
        return expr.id

    def int_const(self, expr):
        return expr.value
    
    def bool_const(self, expr):
        return expr.value
