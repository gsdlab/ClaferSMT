'''
Created on Mar 23, 2013

@author: ezulkosk
'''

class GCard(object):
    '''
    classdocs
    '''


    def __init__(self, isKeyword, interval):
        self.isKeyword = isKeyword
        self.interval = interval
      
      
    def __str__(self):
        s = "(" + str(self.interval[0]) + "," + str(self.interval[1]) + ")"
        return s
    
    def toString(self, level):
        print("A")