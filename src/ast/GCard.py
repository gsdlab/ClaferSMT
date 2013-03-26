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
        return self.interval +"" 