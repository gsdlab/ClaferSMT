'''
Created on Mar 23, 2013

@author: ezulkosk

testing front
'''
from z3 import *


import imp
import sys
import visitors.Visitor
import visitors.PrettyPrint


def main(args):
    src = imp.load_source("ClaferOutput",
                          '/home/ezulkosk/clafer/test/positive/simp.py' )
    module = src.getModule()
    visitors.Visitor.visit(visitors.PrettyPrint.PrettyPrint(), module)
    



if __name__ == '__main__':
    main(sys.argv[1:])
