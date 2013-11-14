'''
Created on Oct 30, 2013

@author: ezulkosk
'''

class SimpleTree():
    
    def __init__(self):
        self.nodes = {}
        self.refs = {}
        self.roots = []
        
    def addNode(self, node, parent):
        if parent:
            if not self.nodes.get(parent):  
                self.nodes[parent] = [node]
            else:   
                self.nodes[parent].append(node)
            self.nodes[node] = []
        else:
            self.nodes[node] = []
    
    def addRef(self, node, ref):
        if self.refs.get(node):
            self.refs[node].append(ref)
        else:
            self.refs[node] = [ref]
    
    def addChild(self, node, child):
        self.nodes[node] = self.nodes[node].append(child)
    
    def addRoot(self, root):
        self.roots.append(root)