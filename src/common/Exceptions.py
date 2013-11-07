'''
Created on Nov 6, 2013

@author: ezulkosk
'''

class UnusedAbstractException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
