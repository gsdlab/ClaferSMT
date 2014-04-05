'''
Created on Apr 4, 2014

@author: ezulkosk
'''
import mlpy


class Classifier():
    def __init__(self):
        pass
    
    def learn(self, data, labels):
        self.classifier.learn(data, labels)
        

class SVM(Classifier):
    def __init__(self, options):
        self.options = options
        self.classifier = mlpy.LibSvm()
        
        
class ClassTree(Classifier):
    def __init__(self, options):
        self.options = options
        self.classifier = mlpy.ClassTree()