'''
Created on Oct 30, 2013

@author: ezulkosk
'''
import sys



class SimpleTree():
    
    def __init__(self):
        self.nodes = []
        self.refs = []
        self.roots = []
        self.abstractRefs = []
        
    def addAbstractRef(self, node, abs_ref):
        self.findParentInList(node, self.abstractRefs)
        self.abstractRefs.append((node, abs_ref))
    
    def findParentInList(self, parent, l):
        (sort, inst) = parent
        for i in l:
            ((currsort, currinst), _) = i
            if sort == currsort and str(inst) == str(currinst):
                #print("found: "  + str(parent) + str(currinst))
                return i
        return None
    
    def addNode(self, node, parent):
        if parent:
            parchildren = self.findParentInList(parent, self.nodes)
            #print("B")
            #print(parchildren)
            #print(parent)
            #print(str(parchildren))
            if parchildren:  
                (_, children) = parchildren
                children.append(node)
            else:   
                sys.exit("Should never happen")
                self.nodes.append((parent, [node]))
        self.nodes.append((node,[]))
    
    def addRef(self, node, ref):
        #import visitors.PrintHierarchy
        parchildren = self.findParentInList(node, self.refs)
        if parchildren:
            (_, children) = parchildren
            children.append(ref)
        else:
            self.refs.append((node, [ref])) #[node] = [visitors.PrintHierarchy.removePrefix(ref)]
    
    def addChild(self, node, child):
        (_,c) = self.findParentInNodes(node, self.nodes)
        c.append(child)
    
    def addRoot(self, root):
        self.roots.append(root)