'''
Created on April 27, 2013

@author: ezulkosk

testing method for the Z3 backend of Clafer
'''
from common import Z3Instance
from visitors import Visitor, PrettyPrint, CreateSorts, \
    CreateBracketedConstraints, CreateCardinalityConstraints, CreateHierarchy
from z3 import *
import common.Common
import imp

def main(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferZ3.
    '''
    
    src = imp.load_source("ClaferOutput",
                          #'/home/ezulkosk/myclafers/nonewline.py')
                          #'/home/ezulkosk/myclafers/simple.py')
                          #'/home/ezulkosk/myclafers/supersimple2.py')
                          #'/home/ezulkosk/myclafers/supersimple.py')
                          #'/home/ezulkosk/myclafers/car.py')
                          #'/home/ezulkosk/myclafers/iso.py')
                          #'/home/ezulkosk/myclafers/bigiso.py')
                          #'/home/ezulkosk/myclafers/bigiso2.py')
                          '/home/ezulkosk/myclafers/constraint.py')
    module = src.getModule()
    
    z3 = Z3Instance.Z3Instance()
    #print(z3)
    z3.run(module, True)
   
if __name__ == '__main__':
    main(sys.argv[1:])
