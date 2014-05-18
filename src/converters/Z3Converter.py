'''
Created on May 14, 2014

@author: ezulkosk
'''
from z3 import *

class Z3Converter():
    
    def if_expr(self, expr):
        try:
            b = expr.bool_expr.convert(self)
        except:
            b = expr.bool_expr
        try:
            t = expr.true_expr.convert(self)
        except:
            t = expr.true_expr
        try:
            f = expr.false_expr.convert(self)
        except:
            f = expr.false_expr
        return If(b,t,f)

    
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
        try:
            l = expr.left.convert(self)
        except:
            l = expr.left
        try:
            r = expr.right.convert(self)
        except:
            r = expr.right
        return Xor(l,r)
    
    def and_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return And(*newList)

    def or_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return Or(*newList)
    
    def sum_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        return Sum(*newList)
    
    def int_var(self, expr):
        return Int(expr.id)

    def int_const(self, expr):
        return expr.value
    
    def bool_expr(self, expr):
        return Bool(expr.id)
    
    
    
    
    
    
    