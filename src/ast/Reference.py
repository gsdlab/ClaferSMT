'''
Created on Mar 23, 2013

@author: ezulkosk
'''

class Reference(object):
    '''
    All variables analogous to those described in IntClafer.hs
    '''


    def __init__(self, isSet, element):
        self.isSet = isSet
        self.element = element

    def __str__(self):
        return self.element
