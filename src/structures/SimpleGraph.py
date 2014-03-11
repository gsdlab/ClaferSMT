'''
Created on Mar 7, 2014

@author: ezulkosk
'''
import collections

class Graph:
    
    def __init__(self):
        self.vertices = {}
        self.degrees = {}
        self.clauses = {}
        self.adjacencycounts = {}
        self.adjacency = collections.defaultdict(set)
        
    def addVertex(self, v):
        if self.clauses.get(v):
            self.clauses[v] = self.clauses[v] + 1
        else:
            self.clauses[v] = 1
        
    def addAdjacent(self, v1, v2):    
        self.adjacency[v1].add(v2)
        acstr = str(v1) + "#" + str(v2)
        if self.adjacencycounts.get(acstr):
            self.adjacencycounts[acstr] = self.adjacencycounts[acstr] + 1
        else:
            self.adjacencycounts[acstr] = 1
    
    def addEdge(self, clause):
        for i in clause:
            self.addVertex(i)
        for i in clause:
            for j in clause:
                if i != j:
                    self.addAdjacent(i, j)