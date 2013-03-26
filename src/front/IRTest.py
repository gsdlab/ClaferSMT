'''
Created on Mar 23, 2013

@author: ezulkosk
'''
from ast import *
import imp
import sys

def main(args):
    #print (args[0])
    #src = imp.load_source("input", args[0])
    src = imp.load_source("ClaferOutput",
                          'C:\\Users\\ezulkosk\\git\\clafer\\test\\positive\\books_tutorial.py' )
    module = src.getModule()
    print(module)

if __name__ == '__main__':
    main(sys.argv[1:])
