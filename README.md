PythonIR
========

Python IR classes for Clafer, as well as Z3 backend

To execute:

Checkout python branch of Clafer project from github.

Once compiled, given a Clafer input file X.cfr, run:
  clafer -mpython X.cfr

This will produce the file X.py within the same directory as X.cfr. For the current implementation, run:
  python IRTest X.py
which will produce the AST in python and print the tree.
