'''
Created on April 27, 2013

@author: ezulkosk

'''
import cProfile
import imp
import sys

from common import Common, Options
from front import UnscopedInstance



def run(args):
    '''
    :param args: Python output file of the Clafer compiler. Generated with argument "-m python".
    :type args: file
    
    Starting point for ClaferSMT.
    '''
    file = Options.FILE
    module = Common.parse(file)
    model = UnscopedInstance.UnscopedInstance(module)
    #model = ClaferModel(module)
    model.run()
       
def main():
    Options.setCommandLineOptions()
    if Options.CPROFILING:
        cProfile.run("main(sys.argv[1:])", sort=1)
    else:
        run(sys.argv[1:])

if __name__ == '__main__':
    main()
    sys.exit()
    
