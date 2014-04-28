'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Common, Options
from front import TestClafers, ModelStats
from front.Z3Instance import Z3Instance
import cProfile
import imp
import sys






    
def run(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
    if Options.MODE == Common.TEST:
        TestClafers.run()
    elif Options.MODE == Common.ONE:
        TestClafers.runForOne()
    elif Options.MODE == Common.ALL:
        TestClafers.runForAll()
    elif Options.MODE in [Common.NORMAL, Common.EXPERIMENT, Common.DEBUG, Common.REPL, Common.MODELSTATS]:
        file = Options.FILE
        module = Common.load(file)
        z3 = Z3Instance(module)
        z3.run()
        
if __name__ == '__main__':
    Options.setCommandLineOptions()
    if Options.CPROFILING:
        cProfile.run("main(sys.argv[1:])", sort=1)
    else:
        run(sys.argv[1:])
