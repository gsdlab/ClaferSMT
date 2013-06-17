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

#abstract x 4
#  c 1..3
#A -> x 3
#  [#this.c = 2]
#B -> x 2
#[B.c = 5]

def get_models(s, M):
        result = []
        count = 0
        #s = Solver()
        #s.add(F)
        while True:
            if s.check() == sat and count != M:
                m = s.model()
                result.append(m)
                #print(m)
                
                # Create a new constraint the blocks the current model
                block = []
                #print("A")
                for d in m:
                    #print(d)
                    # d is a declaration
                    if d.arity() > 0:
                        continue#raise Z3Exception("uninterpreted functions are not supported")
                    # create a constant from declaration
                    c = d()
                    if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                        raise Z3Exception("arrays and uninterpreted sorts are not supported")
                    block.append(c != m[d])
                    print(str(d) + " = " + str(m[d]))
                    #print("C")
                s.add(Or(block))
                count += 1
            else:
                if count == 0:
                    print("UNSAT")
                return result
          
#abstract x 4
#  c 1..3
#A -> x 3
#  [#this.c = 2]
#B -> x 2
#[B.c = 5]  
def main(args):
    #self.bits = [BitVec(self.element.uid.split("_",1)[1] + "$"+str(i), 1) \
    #                 for i in range(self.partitions * self.partitionSize)]#
    A_refs = [Int("A_ref$" + str(i)) for i in range(3)]
    B_refs = [Int("B_ref$" + str(i)) for i in range(2)]
    x_array = [Int("x$" + str(i)) for i in range(4)]
    c_array = [Int("c$" + str(i)) for i in range(12)] 
    
    x_c = Function("x_c", IntSort(), IntSort())
    tot_b_c = Function("tot_b_c", IntSort(), IntSort())
    s = Solver()
    #bound A and B ref to the domain of x
    s.add(*[i <= 3 for i in A_refs])
    s.add(*[i <= 3 for i in B_refs])
    s.add(*[i >= 0 for i in A_refs])
    s.add(*[i >= 0 for i in B_refs])
    
    #bound x,c to [0,1]//will eventually use bits for this
    s.add(*[i >= 0 and i <= 1 for i in x_array + c_array])
  
    #uniquenenss constraints for A and B
    for i in A_refs:
        for j in A_refs:
            if not(i is j):
                s.add(i != j)
    for i in B_refs:
        for j in B_refs:
            if not(i is j):
                s.add(i != j)
    print(s.sexpr())
    s.add(*[x_c(i) == Sum(c_array[3*i:3*(i+1)]) for i in range(4)])
    s.add(*[x_c(i) == 2 for i in A_refs])
    
    s.add(tot_b_c(0) == Sum(*[x_c(i) for i in B_refs]))
    s.add(tot_b_c(0) == 5)
    
    
    #s.add(*[x_c(i) == c_array[3*i:3*i+1] for i in range(4)])
    print(s.check())
    
    get_models(s, 1)

if __name__ == '__main__':
    main(sys.argv[1:])
