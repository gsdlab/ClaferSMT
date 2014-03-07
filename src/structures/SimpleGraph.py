'''
Created on Mar 7, 2014

@author: ezulkosk
'''
import collections

class Graph:
    
    def __init__(self):
        self.vertices = {}
        self.edges = []
        self.degrees = {}
        self.clauses = {}
        self.adjacency = collections.defaultdict(set)
        
    def addVertex(self, v):
        if self.clauses.get(v):
            self.clauses[v] = self.clauses[v] + 1
        else:
            self.clauses[v] = 1
            
    
    def addAdjacent(self, v1, v2):    
        self.adjacency[v1].add(v2)
    
    def addEdge(self, clause):
        for i in clause:
            self.addVertex(i)
        for i in clause:
            for j in clause:
                if i != j:
                    self.addAdjacent(i, j)