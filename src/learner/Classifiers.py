'''
Created on Apr 4, 2014

@author: ezulkosk
'''
import mlpy
import numpy as np
import matplotlib.pyplot as plt



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
        
def test():
    np.random.seed(0)
    mean1, cov1, n1 = [1, 5], [[1,1],[1,2]], 200  # 200 samples of class 1
    x1 = np.random.multivariate_normal(mean1, cov1, n1)
    y1 = np.ones(n1, dtype=np.int)
    mean2, cov2, n2 = [2.5, 2.5], [[1,0],[0,1]], 300 # 300 samples of class 2
    x2 = np.random.multivariate_normal(mean2, cov2, n2)
    y2 = 2 * np.ones(n2, dtype=np.int)
    mean3, cov3, n3 = [6, 8], [[0.5,0],[0,0.5]], 200 # 200 samples of class 3
    x3 = np.random.multivariate_normal(mean3, cov3, n3)
    y3 = 3 * np.ones(n3, dtype=np.int)
    x = np.concatenate((x1, x2, x3), axis=0) # concatenate the samples
    y = np.concatenate((y1, y2, y3))
    tree = mlpy.ClassTree(minsize=10)
    tree.learn(x, y)
    xmin, xmax = x[:,0].min()-1, x[:,0].max()+1
    ymin, ymax = x[:,1].min()-1, x[:,1].max()+1
    xx, yy = np.meshgrid(np.arange(xmin, xmax, 0.1), np.arange(ymin, ymax, 0.1))
    xnew = np.c_[xx.ravel(), yy.ravel()]
    ynew = tree.pred(xnew).reshape(xx.shape)
    ynew[ynew == 0] = 1 # set the samples with no unique classification to 1
    fig = plt.figure(1)
    #cmap = plt.set_cmap(plt.cm.Paired)
    plot1 = plt.pcolormesh(xx, yy, ynew)
    plot2 = plt.scatter(x[:,0], x[:,1], c=y)
    print(tree)
    plt.show()
        