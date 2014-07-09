'''
Created on Mar 26, 2013

@author: ezulkosk
'''
class RealLiteral(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self,value):
        self.value=value
        
    def __str__(self):
        return str(self.value)
        