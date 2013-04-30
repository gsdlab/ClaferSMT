'''
Created on April 27, 2013

@author: ezulkosk

testing method for the Z3 backend of Clafer
'''
from common import Z3Instance
from visitors import Visitor, PrettyPrint, CreateSorts, CreateConstraints, \
    CreateCardinalityConstraints
from z3 import *
import common.Common
import imp






def main(args):
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
                          '/home/ezulkosk/myclafers/integerconstraints.py')
    module = src.getModule()
    #Visitor.visit(PrettyPrint.PrettyPrint(), module)
    z3 = Z3Instance.Z3Instance()
    Visitor.visit(CreateSorts.CreateSorts(z3), module)
    Visitor.visit(CreateConstraints.CreateConstraints(z3), module)
    Visitor.visit(CreateCardinalityConstraints.CreateCardinalityConstraints(z3), module)
    print(z3.getSorts())
    print(z3.getConstraints())
    



if __name__ == '__main__':
    main(sys.argv[1:])
