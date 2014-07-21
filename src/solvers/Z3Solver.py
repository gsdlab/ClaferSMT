'''
Created on May 14, 2014

@author: ezulkosk
'''
from common import Common, SMTLib
from solvers.BaseSolver import BaseSolver
from z3 import *

class Z3Solver(BaseSolver):
    def __init__(self):
        self.converter = Z3Converter()
        self.solver = z3.Solver()
        
    def add(self, constraint):
        self.solver.add(constraint.convert(self.converter))
    
    def convert(self, constraint):
        return constraint.convert(self.converter)
    
    def addRaw(self, constraint):
        '''
        Adds a pre-converted constraint. Should be avoided when possible.
        '''
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
        #self.solver.help()
        self.solver.set(unsat_core=True)
        #self.solver.set("qi_profile",True)
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

    def __init__(self):
        self.num_hit = 0
        self.num_miss = 0
        self.expr_cache = {}

    #keys are sorted tuples of children id's, with the op name as the last element
    

    def checkCache(self, op, children, sort = True):
        if sort:
            #can only sort children for certain operations
            children = sorted([id(i) for i in children])
        else:
            children = [id(i) for i in children]
        children.append(op)
        tup_key = tuple(children)
        expr = self.expr_cache.get(tup_key)
        if(expr):
            #cache hit!
            self.num_hit +=1
            return (True, expr)
        else:
            self.num_miss += 1
            return (False, tup_key)

    def cache(self, expr, tup_key):        
        self.expr_cache[tup_key] = expr
        return expr

    def eq_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("EQ", [l,r])
        if hit:   
            return result
        else:
            return self.cache(l == r, result)

    def ne_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        #print("NEl: " + str(l))
        #print("NEr: " + str(r))
        (hit, result) = self.checkCache("NE", [l,r])
        if hit:   
            return result
        else:
            return self.cache(l != r, result)

    def if_expr(self, expr):
        b = expr.bool_expr.convert(self)
        t = expr.true_expr.convert(self)
        f = expr.false_expr.convert(self)
        (hit, result) = self.checkCache("If", [b,t,f], sort=False)
        if hit:   
            return result
        else:
            return self.cache(If(b,t,f), result)

    def implies_expr(self, expr):
        if expr.unsat_core_implies:
            #left is already converted
            l = expr.left
        else:
            l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("Implies", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(Implies(l,r), result)
    
    def le_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("LE", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l <= r, result)
    
    def lt_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("LT", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l < r, result)
    
    def ge_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("GE", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l >= r, result)
    
    def gt_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("GT", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l > r, result)
    
    def xor_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("Xor", [l,r])
        if hit:   
            return result
        else:
            return self.cache(Xor(l,r), result)
        return Xor(l,r)
    
    def and_expr(self, expr):
        #SMTLib.toStr(expr)
        newList = []
        for i in expr.list:
            val = i.convert(self)
            if not val:
                return False
            else:
                newList.append(val)
        if not newList:
            return True
        (hit, result) = self.checkCache("And", newList)
        if hit:   
            return result
        else:
            return self.cache(And(*newList), result)

    def or_expr(self, expr):
        newList = []
        for i in expr.list:
            val = i.convert(self)
            if not val:
                continue
            else:
                newList.append(val)
        if not newList:
            return False
        (hit, result) = self.checkCache("Or", newList)
        if hit:   
            return result
        else:
            return self.cache(Or(*newList), result)
    
    def sum_expr(self, expr):
        newList = [i.convert(self) for i in expr.list]
        
        (hit, result) = self.checkCache("Sum", newList)
        if hit:   
            return result
        else:
            try:
                ret = Sum(*newList)
            except:
                ret = sum(newList)
            return self.cache(ret, result)
            
        return self.cache(ret, "Sum", newList)

    def plus_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("Plus", [l,r])
        if hit:   
            return result
        else:
            return self.cache(l + r, result)

    def minus_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("Minus", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l - r, result)
        

    def times_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("Times", [l,r])
        if hit:   
            return result
        else:
            return self.cache(l * r, result)
    
    def divide_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("Divide", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l / r, result)

    def intdivide_expr(self, expr):
        l = expr.left.convert(self)
        r = expr.right.convert(self)
        (hit, result) = self.checkCache("IntDivide", [l,r], sort=False)
        if hit:   
            return result
        else:
            return self.cache(l // r, result)

    def neg_expr(self, expr):
        val = expr.value.convert(self)
        (hit, result) = self.checkCache("Neg", [val])
        if hit:   
            return result
        else:
            return self.cache(-(val), result)
    
    def not_expr(self, expr):
        val = expr.value.convert(self)
        (hit, result) = self.checkCache("Not", [val])
        if hit:   
            return result
        else:
            return self.cache(Not(val), result)

    def int_var(self, expr):
        if not expr.bits:
            return Int(expr.id)
        else:
            #use bitvectors
            return BitVec(expr.id, expr.bits)
    
    def real_var(self, expr):
        return Real(expr.id)
    
    def bool_var(self, expr):
        return Bool(expr.id)

    def int_const(self, expr):
        return expr.value
    
    def bool_const(self, expr):
        return expr.value
    
    