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
        #set to a positive number if the training set only contains 1 label
        self.single_label = -1
    
    def learn(self, data, labels):
        if len(set(labels)) == 1:
            self.single_label = labels[0]
        else:
            self.classifier.learn(data, labels)
        
    def predict(self, parameters):
        if self.single_label < 0:
            return self.classifier.pred(parameters)
        else:
            return self.single_label
    
    def getCoefficients(self):
        sys.exit("Get coefficients not supported for the specified Classifier: " + str(self))
        

class LDAC(Classifier):
    def __init__(self, options):
        self.options = options
        self.classifier = mlpy.LDAC()
        super().__init__()
    
    def getCoefficients(self):
        if self.single_label < 0:
            return [0]
        return self.classifier.w()
    
    def __str__(self):
        return "LDAC"
        

class SVM(Classifier):
    def __init__(self, options):
        self.options = options
        super().__init__()
        sys.exit("SVM Not implemented")
        #self.classifier = mlpy.LibSvm()
        
    def __str__(self):
        return "SVM"
        
class ClassTree(Classifier):
    def __init__(self, options):
        self.options = options
        super().__init__()
        sys.exit("ClassTree Not implemented")
        #self.classifier = mlpy.ClassTree()
        
        
    def __str__(self):
        return "ClassTree"