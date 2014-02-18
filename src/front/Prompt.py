'''
Created on Jan 17, 2014

@author: ezulkosk
'''
import cmd, sys
from turtle import *

class TurtleShell(cmd.Cmd):
    intro = 'Welcome to ClaferZ3. Type help or ? to list commands.\n'
    prompt = '(ClaferZ3) '
    file = None

    # ----- basic turtle commands -----
    def do_next(self, arg):
        next()