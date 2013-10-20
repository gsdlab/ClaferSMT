'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Z3Instance, Common, Options
from test import TestClafers, bracketedconstraint_this, multiple_joins, \
    this_dot_parent, arithmetic, relations, boolean_connectives, union, \
    simple_abstract, some, simple_set, zoo, integer_refs, simple_zoo, \
    phone_feature_model, higher_inheritance, this_integer_relation, equal_references
from z3 import get_version_string
import sys
import cProfile





def main(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
    Common.MODE = Options.MODE 
    
    if Common.MODE == Common.TEST:
        TestClafers.run()
    else:
        module = Options.MODULE
        
        z3 = Z3Instance.Z3Instance(module)
        z3.run()
        #z3.run()
        
        
   
if __name__ == '__main__':
    if Options.CPROFILING:
        cProfile.run("main(sys.argv[1:])", sort=1)
    else:
        main(sys.argv[1:])
