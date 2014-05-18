'''
Created on May 14, 2014

@author: ezulkosk
'''
from z3 import *

class Z3Converter():
    
    def if_expr(self, expr):
        pass
    
    def implies_expr(self, expr):
        try:
            l = expr.left.convert(self)
        except:
            l = expr.left
        try:
            r = expr.right.convert(self)
        except:
            r = expr.right    
        return Implies(l, r)
    
    def le_expr(self, expr):
        try:
            l = expr.left.convert(self)
        except:
            l = expr.left
        try:
            r = expr.right.convert(self)
        except:
            r = expr.right    
        return l <= r
    
    def lt_expr(self, expr):
        try:
            l = expr.left.convert(self)
        except:
            l = expr.left
        try:
            r = expr.right.convert(self)
        except:
            r = expr.right    
        return l < r
    
    def xor_expr(self, expr):
        pass
    
    def and_expr(self, expr):
        pass

    def or_expr(self, expr):
        pass
    
    def sum_expr(self, expr):
        pass
    
    def int_var(self, expr):
        return Int(expr.id)
    
    def bool_expr(self, expr):
        pass
    
    
    
    
    
    
    