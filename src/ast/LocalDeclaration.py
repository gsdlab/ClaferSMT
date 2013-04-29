'''
Created on Mar 24, 2013

@author: ezulkosk
'''

class LocalDeclaration(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, element):
        self.element = element
        
    def __str__(self):
        return self.element
    