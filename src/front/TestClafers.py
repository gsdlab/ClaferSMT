'''
Created on Sep 15, 2013

@author: ezulkosk
'''
from common import Options
from common.Clock import Clock
from front.Z3Instance import Z3Instance


SEPARATOR = "========================================================" 
def print_separate(x):
    print("\n" + SEPARATOR + "\n| " + x + "\n" +  SEPARATOR + "\n")

def getTestSet():
    if Options.TEST_SET == Options.MY_TESTS:
        return Options.my_tests
    elif Options.TEST_SET == Options.POSITIVE_TESTS:
        return Options.positive_tests
        
def run():
    '''
    Runs the Z3-translator on each pair (file, numInstances) in tests, 
    and ensures that the number of generated models equals numInstances.
    '''
    clock = Clock()
    tests = getTestSet()
    num_passed = 0
    temp_model_count = Options.NUM_INSTANCES
    for t in tests:
        (file, expected_model_count) = t
        if expected_model_count == Options.INFINITE and Options.NUM_INSTANCES < 0:
            #will change it back after the test runs
            Options.NUM_INSTANCES = 3
        module = file.getModule()
        print_separate("Attempting: " + str(file.__name__))
        clock.tick("Total Z3 Run Time")
        z3 = Z3Instance(module)
        actual_model_count = z3.run()
        clock.tack("Total Z3 Run Time")
        clock = clock.combineClocks(z3.clock)
        if(expected_model_count == actual_model_count or 
           (expected_model_count == Options.INFINITE and actual_model_count == Options.NUM_INSTANCES)):
            print("PASSED: " + str(file))
            num_passed = num_passed + 1
        else:
            print("FAILED: " + str(file) + " " + str(expected_model_count) + " " + str(actual_model_count))
        Options.NUM_INSTANCES = temp_model_count
    print_separate("Results: " + str(num_passed) + "/" + str(len(tests)))   
    clock.printEvents()
       
       
def runAndOutputModels():
    clock = Clock()
    tests = getTestSet()
    for t in tests:
        (file, _) = t
        module = file.getModule()
        print_separate("Attempting: " + str(file.__name__))
        clock.tick("Total Z3 Run Time")
        z3 = Z3Instance(module)
        z3.run()
        clock.tack("Total Z3 Run Time")
        clock = clock.combineClocks(z3.clock)
    print_separate("Results: ")  
    clock.printEvents()
        
def runForOne():  
    '''
    Runs the Z3-translator on each pair file in tests, 
    and outputs one model for each, if satisfiable.
    '''  
    Options.NUM_INSTANCES = 1
    runAndOutputModels()
    
def runForAll():
    '''
    Runs the Z3-translator on each pair file in tests, 
    and outputs all model for each, if satisfiable (limited if infinite models).
    '''
    runAndOutputModels()