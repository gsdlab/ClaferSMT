'''
Created on May 14, 2014

@author: ezulkosk
'''
from z3 import *

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
        #print([i for i in expr.list])
        #print(*newList)
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
        return expr.val

    def int_const(self, expr):
        return expr.value
    
    def bool_const(self, expr):
        return expr.value
    
    
    def bool_expr(self, expr):
        return Bool(expr.id)


    
    
    
    
    
    
    