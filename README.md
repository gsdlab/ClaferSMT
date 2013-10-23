PythonIR
========

Python IR classes for Clafer, as well as Z3 backend

To execute:

Checkout python branch of Clafer project from github.

Once compiled, given a Clafer input file X.cfr, run:
  clafer -mpython X.cfr

This will produce the file X.py within the same directory as X.cfr. For the current implementation, run:
  python Z3Run.py X.py
which will produce the AST in python and print the tree.

Required
========

Python 3

Z3 4.2.3

pip install bintrees (make sure it is installed for the correct version of python).

Remove the warning messages from bintrees imports.

Depending on your version of python, you may need to install lxml for "basestring" to work.
