'''
Created on Sep 15, 2013

@author: ezulkosk
'''
from common import Z3Instance
from test import multiple_joins, bracketedconstraint_this, this_dot_parent, \
    arithmetic, relations, boolean_connectives, union, simple_abstract, some, \
    simple_set, integer_refs, higher_inheritance

tests = [ 
          (multiple_joins, 1),
          (bracketedconstraint_this, 6),
          (this_dot_parent, 2),
          (arithmetic, 2),
          (relations, 1),
          (boolean_connectives, 2),
          (union, 6),
          (simple_abstract, 0),
          (some, 1),
          (simple_set, 6),
          (integer_refs, 1),
          (higher_inheritance, 1)
         ]

def run():
    '''
    Runs the Z3-translator on each pair (file, numInstances) in tests, 
    and ensures that the number of generated models equals numInstances.
    '''
    count = 0
    for t in tests:
        count = count+1
        (file, expected_model_count) = t
        module = file.getModule()
        z3 = Z3Instance.Z3Instance(module)
        actual_model_count = z3.run()
        
        if(expected_model_count == actual_model_count):
            print("PASSED: " + str(file))
        else:
            print("FAILED: " + str(file) + " " + str(expected_model_count) + " " + str(actual_model_count))