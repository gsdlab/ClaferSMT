'''
Created on Mar 23, 2013

@author: ezulkosk
'''
#from z3 import *
from ast import *
from visitors.PrettyPrint import PrettyPrint
import imp
import sys
import visitors.Visitor



def main(args):
    #print (args[0])
    src = imp.load_source("input", args[0])

    
    #x = Int('x')
    #y = Int('y')
    #solve(x > 2, y < 10, x + 2*y == 7)
    #src = imp.load_source("ClaferOutput",
    #                      'C:\\Users\\ezulkosk\\git\\clafer\\test\\positive\\books_tutorial.py' )
    module = src.getModule()
    print("A")
    visitors.Visitor.visit(visitors.PrettyPrint.PrettyPrint(), module)
    



if __name__ == '__main__':
    main(sys.argv[1:])
