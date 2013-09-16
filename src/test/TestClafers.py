'''
Created on Sep 15, 2013

@author: ezulkosk
'''
from common import Z3Instance
from test import multiple_joins, bracketedconstraint_this, this_dot_parent

tests = [ 
          (multiple_joins, 1),
          (bracketedconstraint_this, 6),
          (this_dot_parent, 2)
         ]

def run():
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