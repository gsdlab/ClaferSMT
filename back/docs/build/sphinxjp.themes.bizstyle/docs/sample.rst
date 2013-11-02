======
Sample
======


Literal Block
=============

.. code-block:: python

   import sys

   Usage = """
   Usage:
   $ python factorial.py
   """

   def fact(x):
       if x == 0:
           return 1
       else:
           return x * fact(x-1)

   if (len(sys.argv)>1) :
       print fact(int(sys.argv[1]))
   else:
       print Usage


Admonitions
===========

.. danger::
   This is sample of "Danger" admonition directive.

.. error::
   This is sample of "Error" admonition directive.

.. warning::
   This is sample of "Warning" admonition directive.

.. caution::
   This is sample of "Caution" admonition directive.

.. attention::
   This is sample of "Attention" admonition directive.

.. important::
   This is sample of "Important" admonition directive.

.. note::
   This is sample of "Note" admonition directive.

.. hint::
   This is sample of "Hint" admonition directive.

.. tip::
   This is sample of "Tip" admonition directive.

.. admonition:: Here is admonition title

   This is sample of "Admonition" admonition directive.

   - One
   - Two
   - Three


