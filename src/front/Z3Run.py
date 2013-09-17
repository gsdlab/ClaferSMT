'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Z3Instance, Common
from test import TestClafers, bracketedconstraint_this, multiple_joins, \
    this_dot_parent, arithmetic, relations
import sys




def main(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
    Common.MODE = Common.NORMAL
    
    if Common.MODE == Common.TEST:
        TestClafers.run()
    else:
        #module = bracketedconstraint_this.getModule()
        #module = multiple_joins.getModule()
        #module = this_dot_parent.getModule()
        #module = arithmetic.getModule()
        module = relations.getModule()
        z3 = Z3Instance.Z3Instance(module)
        z3.run()
   
if __name__ == '__main__':
    main(sys.argv[1:])
