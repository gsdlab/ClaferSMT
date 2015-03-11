'''
Created on Mar 26, 2013

@author: ezulkosk
'''
import visitors.Visitor
import visitors.ReturnVisitor

class VisitorTemplate(object):
    '''
    *see:* :class:`visitors`
    
    Visitor that simply traverses the Clafer AST, 
    used as a superclass for other visitors
    '''
    def __init__(self):
        pass
    
    def claferVisit(self, element):
        '''
        :param element: A Clafer AST node
        :type element: :class:`~ast.Clafer`
        '''
        visitors.Visitor.visit(self,element.supers)
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def claferidVisit(self, element):
        '''
        :param element: A ClaferId AST node
        :type element: :class:`~ast.ClaferId`
        '''
        pass
    
    def constraintVisit(self, element):
        '''
        :param element: An IRConstraint AST node
        :type element: :class:`~ast.IRConstraint`
        '''
        visitors.Visitor.visit(self, element.exp)
    
    def declarationVisit(self, element):
        '''
        :param element: A Declaration AST node
        :type element: :class:`~ast.Declaration`
        '''
        for i in element.localDeclarations:
            visitors.Visitor.visit(self, i)
        visitors.Visitor.visit(self, element.body)
    
    def declpexpVisit(self, element):
        '''
        :param element: A DeclPExp AST node
        :type element: :class:`~ast.DeclPExp`
        '''
        visitors.Visitor.visit(self, element.declaration)
        visitors.Visitor.visit(self, element.bodyParentExp)
        
    def expVisit(self, element):
        '''
        :param element: A Exp AST node
        :type element: :class:`~ast.Exp`
        '''
        for i in element.iExp:
            visitors.Visitor.visit(self, i)
    
    
    def funexpVisit(self, element):
        '''
        :param element: A FunExp AST node
        :type element: :class:`~ast.FunExp`
        '''
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def gcardVisit(self, element):
        '''
        :param element: A GCard AST node
        :type element: :class:`~ast.GCard`
        '''
        pass
    
    def goalVisit(self, element):
        '''
        :param element: A Goal AST node
        :type element: :class:`~ast.Goal`
        '''
        visitors.Visitor.visit(self, element.exp)
    
    def localdeclarationVisit(self, element):
        '''
        :param element: A LocalDeclaration AST node
        :type element: :class:`~ast.LocalDeclaration`
        '''
        pass
    
    def moduleVisit(self, element):
        '''
        :param element: A Module AST node
        :type element: :class:`~ast.Module`
        '''
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def supersVisit(self, element):
        '''
        :param element: A Supers AST node
        :type element: :class:`~ast.Supers`
        '''
        for i in element.elements:
            visitors.Visitor.visit(self, i)
    
    def integerliteralVisit(self, element):
        '''
        :param element: An IntegerLiteral AST node
        :type element: :class:`~ast.IntegerLiteral`
        '''
        pass
        
    def realliteralVisit(self, element):
        '''
        :param element: A RealLiteral AST node
        :type element: :class:`~ast.RealLiteral`
        '''
        pass
        
    def stringliteralVisit(self, element):
        '''
        :param element: A StringLiteral AST node
        :type element: :class:`~ast.StringLiteral`
        '''
        pass
    
    def noneVisit(self):
        pass
    
class ReturnVisitorTemplate(object):
    '''
    *see:* :class:`visitors`
    
    Visitor that simply traverses the Clafer AST, 
    used as a superclass for other visitors
    '''
    def __init__(self):
        pass
    
    def claferVisit(self, element):
        '''
        :param element: A Clafer AST node
        :type element: :class:`~ast.Clafer`
        '''
        return element
    
    def claferidVisit(self, element):
        '''
        :param element: A ClaferId AST node
        :type element: :class:`~ast.ClaferId`
        '''
        return element
    
    def constraintVisit(self, element):
        '''
        :param element: An IRConstraint AST node
        :type element: :class:`~ast.IRConstraint`
        '''
        return element
    
    def declarationVisit(self, element):
        '''
        :param element: A Declaration AST node
        :type element: :class:`~ast.Declaration`
        '''
        res = []
        for i in element.localDeclarations:
            res.append(visitors.ReturnVisitor.visit(self, i))
        res.append(visitors.ReturnVisitor.visit(self, element.body))
        return res
    
    def declpexpVisit(self, element):
        '''
        :param element: A DeclPExp AST node
        :type element: :class:`~ast.DeclPExp`
        '''
        res = []
        res.append(visitors.ReturnVisitor.visit(self, element.declaration))
        res.append(visitors.ReturnVisitor.visit(self, element.bodyParentExp))
        
    def expVisit(self, element):
        '''
        :param element: A Exp AST node
        :type element: :class:`~ast.Exp`
        '''
        res = []
        for i in element.iExp:
            res.append(visitors.ReturnVisitor.visit(self, i))
        return res
    
    
    def funexpVisit(self, element):
        '''
        :param element: A FunExp AST node
        :type element: :class:`~ast.FunExp`
        '''
        res = []
        for i in element.elements:
            res.append(visitors.ReturnVisitor.visit(self, i))
        return res
    
    def gcardVisit(self, element):
        '''
        :param element: A GCard AST node
        :type element: :class:`~ast.GCard`
        '''
        return element
    
    def goalVisit(self, element):
        '''
        :param element: A Goal AST node
        :type element: :class:`~ast.Goal`
        '''
        return visitors.ReturnVisitor.visit(self, element.exp)
    
    def localdeclarationVisit(self, element):
        '''
        :param element: A LocalDeclaration AST node
        :type element: :class:`~ast.LocalDeclaration`
        '''
        return element
    
    def moduleVisit(self, element):
        '''
        :param element: A Module AST node
        :type element: :class:`~ast.Module`
        '''
        res = []
        for i in element.elements:
            r = visitors.ReturnVisitor.visit(self, i)
            if r:
                res.append(r)
        return res
    
    def supersVisit(self, element):
        '''
        :param element: A Supers AST node
        :type element: :class:`~ast.Supers`
        '''
        supers = []
        for i in element.elements:
            supers.append(visitors.ReturnVisitor.visit(self, i))
        return supers
    
    def integerliteralVisit(self, element):
        '''
        :param element: An IntegerLiteral AST node
        :type element: :class:`~ast.IntegerLiteral`
        '''
        return element
        
    def realliteralVisit(self, element):
        '''
        :param element: A RealLiteral AST node
        :type element: :class:`~ast.RealLiteral`
        '''
        return element
        
    def stringliteralVisit(self, element):
        '''
        :param element: A StringLiteral AST node
        :type element: :class:`~ast.StringLiteral`
        '''
        return element
    
    def noneVisit(self):
        pass
    
    
