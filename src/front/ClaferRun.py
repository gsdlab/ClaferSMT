'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Common, Options
from front import TestClafers, ModelStats
from front.ClaferModel import ClaferModel
import cProfile
import imp
import sys

    
def run(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferSMT.
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
        model = ClaferModel(module)
        model.run()
       
def main():
    Options.setCommandLineOptions()
    if Options.CPROFILING:
        cProfile.run("run(sys.argv[1:])", sort=1)
    else:
        run(sys.argv[1:])

if __name__ == '__main__':
    main()
    