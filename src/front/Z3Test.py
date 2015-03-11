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
    s.add(z3.Not(z3.And(b, c)))
    print(s.check())
    print(s.model())
    m = s.model()
    for i in m:
        print(m[i])
        block = (m[i])
        block = (i != m[i])
        if strblock == True:
            print(block)