'''
Created on Oct 27, 2014

@author: ezulkosk
'''

import z3

if __name__ == '__main__':
    a = z3.Bool("a")
    b = z3.Bool("b")
    c = z3.Bool("c")
    
    s = z3.Solver()
    s.add(z3.Implies(z3.Not(z3.And(a, b)), z3.Not(z3.And(z3.Not(b), c))))
    s.add(z3.Not(z3.Implies(c, b)))
    print(s.check())
    print(s.model())