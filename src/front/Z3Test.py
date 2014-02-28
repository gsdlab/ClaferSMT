'''
Created on April 27, 2013

@author: ezulkosk

testing method for the Z3 backend of Clafer
'''
from z3 import BitVec, Bool, Solver, Xor, Function, IntSort, Array, Int, sat, \
    is_array, Or, Goal, Then, RealVal, Datatype, DeclareSort, Consts, ForAll, Exists, \
    Distinct, Const, Implies, BoolSort, IntSort, And, Or, Not, BitVecs, solve_using
from z3consts import Z3_UNINTERPRETED_SORT
from z3types import Z3Exception
import sys


#abstract x 4
#  c 1..3
#A -> x 3
#  [#this.c = 2]
#B -> x 2
#[B.c = 5]


          
#abstract X 4
#  C 1..3
#  [#this.C = 2]
#B : X 2
#[B.C = 5]  

def BitVecVector(prefix, sz, N):
  """Create a vector with N Bit-Vectors of size sz"""
  return [ BitVec('%s_%s' % (prefix, i), sz) for i in range(N) ]

def main(args):
    s = Solver()
    bv_solver = Then('simplify',
                 'solve-eqs',
                 'bit-blast',
                 'sat').solver()

    x, y = BitVecs('x y', 16)
    solve_using(bv_solver, x | y == 13, x > y)

    '''
    X = DeclareSort('X')
    C = DeclareSort('C')
    #B = DeclareSort('B')
    
    i = Int('i')
    xi, xi2 = Consts('xi xi2', X)
    is_X = Function('is_X', X, BoolSort())
    is_B = Function('is_B', X, BoolSort())
    
    B_is_x = ForAll([xi], Implies(is_B(xi), is_X(xi)))
    s.add(ForAll([xi, xi2], Implies(Distinct(xi, xi2), True)))
    
    crd_B = Int('crd_B')
    ord_B = Function('ord_B', X, IntSort())
    inv_B = Function('inv_B', IntSort(), X)
    
    s.add(And(crd_B >= 0, Implies(crd_B == 0, ForAll([xi], Not(is_B(xi)))))) #5
    s.add(ForAll([xi], Implies(is_B(xi), And(1 <= ord_B(xi), ord_B(xi) <= crd_B)))) #6
    s.add(ForAll([xi], Implies(is_B(xi), inv_B(ord_B(xi)) == xi))) #7
    s.add(ForAll([i], Implies(And(1 <= i, i <= crd_B), ord_B(inv_B(i)) == i))) #8
    s.add(crd_B == 4)
    
    s.check()
    m = s.model()
    
    print(m)
    print(m.eval(inv_B(4)))
    print(m.eval(inv_B(5)))
    print(m.eval(inv_B(1)))
    print(m[X])
    '''
    
    
    '''
    R = RealVal(1/3)
    A = Bool("A")
    B = Bool("B")
    C = Bool("C")
    D = Bool("D")
    x = Int("x")
    y = Int("y")
    s = Solver()
    print(R.sexpr())
    s.check()
    print(s.model());
    g = Goal()
    g.add(x == 0, y >= x + 100000000000000000000)
    
    print(g.depth())
    print(g)
    s.add(g)
    print(s.check())
    r = Then('simplify', 'solve-eqs')(g)
    # r has 1 subgoal
    print(len(r))
    print(r)
    
    f = Function('f', IntSort(), IntSort(), IntSort())
    A = Array("A", IntSort(), IntSort())
    B = Array("B", IntSort(), IntSort())
    s = Solver()
    #c = IntSort()
    print(s.check())
    
    
    m = s.model()
    print(m.eval(A[0]))
    print(m.eval(A[1]))
    print(m.eval(A[2]))
    '''
    '''
    #self.bits = [BitVec(self.element.uid.split("_",1)[1] + "$"+str(i), 1) \
    #                 for i in range(self.partitions * self.partitionSize)]#
    A_refs = [Int("A_ref$" + str(i)) for i in range(3)]
    B_refs = [Int("B_ref$" + str(i)) for i in range(2)]
    x_array = [Int("x$" + str(i)) for i in range(4)]
    c_array = [Int("c$" + str(i)) for i in range(12)] 
    
    x_c = Function("x_c", IntSort(), IntSort())
    s = Solver()
    #bound A and B ref to the domain of x
    s.add(*[i <= 3 for i in A_refs])
    s.add(*[i <= 3 for i in B_refs])
    s.add(*[i >= 0 for i in A_refs])
    s.add(*[i >= 0 for i in B_refs])
    
    #bound x,c to [0,1]//will eventually use bits for this
    s.add(*[i >= 0 and i <= 1 for i in x_array + c_array])
  
    #uniqueneness constraints for A and B
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
    
    s.add(5 == Sum(*[x_c(i) for i in B_refs]))
    
    
    #s.add(*[x_c(i) == c_array[3*i:3*i+1] for i in range(4)])
    print(s.check())
    
    get_models(s, 1)
    '''
    
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
if __name__ == '__main__':
    main(sys.argv[1:])
