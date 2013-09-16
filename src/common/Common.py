'''
Created on Apr 28, 2013

@author: ezulkosk
'''

NORMAL = 0
DEBUG = 1
TEST = 2
MODE = NORMAL

def debug_print(string):
    if(MODE == DEBUG):
        print(string)
        
def standard_print(string):
    if(MODE != TEST):
        print(string)





    