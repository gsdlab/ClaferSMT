'''
Created on May 14, 2014

@author: ezulkosk
'''
from common import Common
from z3 import *

class Z3Solver():
    def __init__(self):
        self.converter = Z3Converter()
        self.solver = z3.Solver()
        
    def add(self, constraint):
        self.solver.add(constraint.convert(self.converter))
    
    def convert(self, constraint):
        return constraint.convert(self.converter)
    
    def addRaw(self, constraint):
        self.solver.add(constraint)
    
    def check(self, unsat_core_trackers=None):
        #print(unsat_core_trackers)
        if unsat_core_trackers:
            if self.solver.check(unsat_core_trackers) == sat:
                return Common.SAT
            else:
                return Common.UNSAT 
        if self.solver.check() == sat:
            return Common.SAT
        else:
            return Common.UNSAT
        
    def setOptions(self):
        self.solver.set(auto_config=False)
        self.solver.set(unsat_core=True)
        self.solver.set(model_completion=True)
        
    def model(self):
        return self.solver.model()

    def unsat_core(self):
        return self.solver.unsat_core()

    def assertions(self):
        return self.solver.assertions()
    
    def push(self):
        self.solver.push()
        
    def pop(self):
        self.solver.pop()
        

class Z3Converter():

    def eq_expr(self, expr):
        return expr.left.convert(self) == expr.right.convert(self)

    def ne_expr(self, expr):
        return expr.left.convert(self) != expr.right.convert(self)

    def if_expr(self, expr):
        b = expr.bool_expr.convert(self)
        t = expr.true_expr.convert(self)
        f = expr.false_expr.convert(self)
        return If(b,t,f)

    def implies_expr(self, expr):
        if expr.unsat_core_implies:
            #left is already converted
            l = expr.left
        else:
            l = expr.left.convert(self)
        r = expr.right.convert(self)
        return Implies(l, r)
    
    def le_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l <= r
    
    def lt_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l < r
    
    def ge_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l >= r
    
    def gt_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l > r
    
    def xor_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return Xor(l,r)
    
    def and_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return And(*newList)

    def or_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return Or(*newList)
    
    def sum_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        try:
            ret = Sum(*newList)
        except:
            ret = sum(newList)
        return ret

    def plus_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l + r

    def minus_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l - r

    def times_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l * r
    
    def divide_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l / r

    def intdivide_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        return l // r

    def neg_expr(self, expr):
        val = expr.value.convert(self)
        return -(val)
    
    def not_expr(self, expr):
        val = expr.value.convert(self)
        return Not(val)

    def int_var(self, expr):
        return Int(expr.id)
    
    def real_var(self, expr):
        return Real(expr.id)
    
    def bool_var(self, expr):
        return Bool(expr.id)

    def int_const(self, expr):
        return expr.value
    
    def bool_const(self, expr):
        return expr.value
    
    
    def bool_expr(self, expr):
        return Bool(expr.id)
    