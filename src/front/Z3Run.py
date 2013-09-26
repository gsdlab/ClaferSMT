'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Z3Instance, Common
from test import TestClafers, bracketedconstraint_this, multiple_joins, \
    this_dot_parent, arithmetic, relations, boolean_connectives, union, \
    simple_abstract, some, simple_set, zoo, integer_refs, simple_zoo, \
    phone_feature_model
from z3 import get_version_string
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
        #module = relations.getModule()
        #module = boolean_connectives.getModule()
        #module = union.getModule()
        #module = simple_abstract.getModule()
        #module = some.getModule()
        #module = simple_set.getModule()
        module = zoo.getModule()
        #module = simple_zoo.getModule()
        #module = integer_refs.getModule()
        #module = phone_feature_model.getModule()
        z3 = Z3Instance.Z3Instance(module)
        z3.run()
   
if __name__ == '__main__':
    main(sys.argv[1:])
