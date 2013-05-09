'''
Created on April 27, 2013

@author: ezulkosk

testing method for the Z3 backend of Clafer
'''
from common import Z3Instance
from visitors import Visitor, PrettyPrint, CreateSorts, \
    CreateBracketedConstraints, CreateCardinalityConstraints, CreateHierarchy
from z3 import *
import common.Common
import imp

def getBit(bitvec, pos):
    bv = BitVecVal(1, bitvec.size())
    return (bitvec & (bv << pos)) >> pos

#exclusive on top
def getBitRange(bitvec, lower, upper):
    num = 0
    bits = upper - lower
    for i in range(bits):
        num += 2 ** i
    print(num)
    bv = BitVecVal(num, bitvec.size())
    return (bitvec & (bv << (bitvec.size() - upper))) >> (bitvec.size() - upper)
        
def main(args):
    A = BitVec('A', 2)
    B = BitVec('B', 6)
    Extract(2,0, B)
    print(getBitRange(B, 0, 3))
    
    C1 = Implies(Extract(0,0, A) == 1, Extract(5,3,B) > 0)

    s = Solver()
    s.add(C1)
    s.check()
    m = s.model()
    print(m.decls())
    print(m[A], m[B])
    
    

if __name__ == '__main__':
    main(sys.argv[1:])
