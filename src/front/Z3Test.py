'''
Created on April 27, 2013

@author: ezulkosk

testing frontend for the Z3 backend of Clafer
'''
from visitors import Visitor, PrettyPrint, DefineSorts, CreateConstraints
from z3 import *
import common.Common
import imp





def main(args):
    A = DeclareSort('A')
    w,x,y,z = Consts('w x y z', A)
    axioms = [ Exists([w,x,y], Distinct(w,x,y)),
               Not(Exists([w,x,y,z], Distinct(w,x,y,z)))
             ]
    s = Solver()
    s.add(axioms)
    print(s.check())
    print(s.model())
    src = imp.load_source("ClaferOutput",
                          #'/home/ezulkosk/myclafers/nonewline.py')
                          '/home/ezulkosk/myclafers/integerconstraints.py')
    module = src.getModule()
    Visitor.visit(PrettyPrint.PrettyPrint(), module)
    Visitor.visit(DefineSorts.DefineSorts(), module)
    Visitor.visit(CreateConstraints.CreateConstraints(), module)
    print(common.Common.getSorts())
    print(common.Common.getConstraints())
   



if __name__ == '__main__':
    main(sys.argv[1:])
