'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Common, Options
from front import TestClafers, ModelStats
from front.Z3Instance import Z3Instance
import cProfile
import sys
import imp





def load(file):
    if file.endswith(".cfr"):
        sys.exit("Run 'clafer --mode=python " + str(file) + "' first.")
    file = imp.load_source("module", str(file))
    module = file.getModule()
    return module
    
def main(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
 
    Common.MODE = Options.MODE 
    if Common.MODE == Common.TEST:
        TestClafers.run()
    elif Common.MODE == Common.ONE:
        TestClafers.runForOne()
    elif Common.MODE == Common.ALL:
        TestClafers.runForAll()
    elif (not Options.ECLIPSE) and (Common.MODE in [Common.NORMAL, Common.EXPERIMENT, Common.DEBUG, Common.REPL, Common.MODELSTATS]):
        file = Options.FILE
        #print(file)
        module = load(file)
        z3 = Z3Instance(module)
        z3.run()
    else:
        module = Options.MODULE()
        
        z3 = Z3Instance(module)
        z3.run()
        #z3.run()
        
        
   
if __name__ == '__main__':
    Options.setCommandLineOptions()
    if Options.CPROFILING:
        cProfile.run("main(sys.argv[1:])", sort=1)
    else:
        main(sys.argv[1:])
