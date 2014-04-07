'''
Created on Apr 4, 2014

@author: ezulkosk
'''

import matplotlib.pyplot as plt
import mlpy
import numpy as np
import sys



class Classifier():
    def __init__(self):
        pass
    
    def learn(self, data, labels):
        self.classifier.learn(data, labels)
        

class LDAC(Classifier):
    def __init__(self, options):
        self.options = options
        self.classifier = mlpy.LDAC()
        

class SVM(Classifier):
    def __init__(self, options):
        self.options = options
        sys.exit("SVM Not implemented")
        #self.classifier = mlpy.LibSvm()
        
        
class ClassTree(Classifier):
    def __init__(self, options):
        self.options = options
        sys.exit("ClassTree Not implemented")
        #self.classifier = mlpy.ClassTree()
        
