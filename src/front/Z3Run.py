'''
Created on April 27, 2013

@author: ezulkosk

'''
from common import Z3Instance, Common
from test import TestClafers
import imp
import sys




def main(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
    Common.MODE = Common.TEST
    
    if Common.MODE == Common.TEST:
        TestClafers.run()
    else:
        src = imp.load_source("ClaferOutput",
                          #'/home/ezulkosk/myclafers/testclafers/py/bracketedconstraint_this.py')
                          '/home/ezulkosk/myclafers/testclafers/py/multiple_joins.py')
        module = src.getModule()
        z3 = Z3Instance.Z3Instance(module)
        z3.run()
   
if __name__ == '__main__':
    main(sys.argv[1:])
