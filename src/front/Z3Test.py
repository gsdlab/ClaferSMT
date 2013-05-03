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

def main(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    Starting point for ClaferZ3.
    
    '''
    #A = DeclareSort('A')
    #w,x,y,z = Consts('w x y z', A)
    #axioms = [ Exists([w,x,y], Distinct(w,x,y)),
    #           Not(Exists([w,x,y,z], Distinct(w,x,y,z)))
    #         ]
    #s = Solver()
    #s.add(axioms)
    #print(s.check())
    #print(s.model())
    src = imp.load_source("ClaferOutput",
                          #'/home/ezulkosk/myclafers/nonewline.py')
                          '/home/ezulkosk/myclafers/simple.py')
    module = src.getModule()
    Visitor.visit(PrettyPrint.PrettyPrint(), module)
    z3 = Z3Instance.Z3Instance()
    Visitor.visit(CreateSorts.CreateSorts(z3), module)
    Visitor.visit(CreateHierarchy.CreateHierarchy(z3), module)
    Visitor.visit(CreateBracketedConstraints.CreateBracketedConstraints(z3), module)
    Visitor.visit(CreateCardinalityConstraints.CreateCardinalityConstraints(z3), module)
    
    #print(z3)
    z3.run(True)
    
    '''
    A = DeclareSort('A')
    A_B = DeclareSort('A.B')
    A_C = DeclareSort('A.C')
    A_C_D = DeclareSort('A.C.D')
    
    _A = Datatype('_A')
    _A_B = Datatype('_A_B')
    _A_C = Datatype('_A_C')
    _A_C_D = Datatype('_A_C_D')
    
    _A.declare('new_A', ('field0', A), ('field1', _A_B), ('field2', _A_C))
    _A_B.declare('new_B', ('field0', A_B))
    _A_C.declare('new_A_C', ('field0', A_C), ('ref', IntSort()), ('field1', _A_C_D))
    _A_C_D.declare('new_A_C_D', ('field0', A_C_D))
    
    _A, _A_B, _A_C, _A_C_D = CreateDatatypes(_A,_A_B, _A_C, _A_C_D)

    a,b,c = Consts('a b c', _A)
    Not(Exists([a,b], Distinct(a,b)))
    a2,b2,c2 = Consts('a2 b2 c2', _A_B)
    solver = Solver()
    solver.add(Distinct(a,b,c))
    print(solver.check())
    m = solver.model()
    print(m[A])
    #print(solver.)
    #solve(Distinct(a,b,c), Distinct(a2,b2,c2))
    '''



if __name__ == '__main__':
    main(sys.argv[1:])
