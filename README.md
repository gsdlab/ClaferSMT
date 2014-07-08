ClaferSMT
=========

v0.3.6.1

Python IR classes for Clafer, as well as Z3 backend

Contributors
------------

* [Ed Zulkoski](http://gsd.uwaterloo.ca/ezulkosk). Main developer.
* [Alexandr Murashkin](http://gsd.uwaterloo.ca/amurashk). Testing.
* [Michał Antkiewicz](http://gsd.uwaterloo.ca/mantkiew). Testing, technology transfer.

Getting the Clafer SMT Backend
------------------------------

### Dependencies for running

Regardless of the installation method, the following are required:

* [Python 3](https://www.python.org/download/releases/3.4.1/) v3.4.1
* [Clafer Compiler](https://github.com/gsdlab/clafer) v0.3.6.1
  * Required for compiling Clafer files (`.cfr`) into the Clafer Python IR format (`.py`), so that they can be run using the tool.
* [Z3 SMT Solver](http://z3.codeplex.com/) v4.2.3
* [bintrees](https://bitbucket.org/mozman/bintrees)
  * pip install bintrees (make sure it is installed for Python 3).
  * (optional): Remove the warning messages from bintrees' imports.

### Installation from binaries

Binary distributions of the release 0.3.6.1 of Clafer Tools for Windows, Mac, and Linux, 
can be downloaded from [Clafer Tools - Binary Distributions](http://http://gsd.uwaterloo.ca/clafer-tools-binary-distributions). 

1. download the binaries and unpack `<target directory>` of your choice
2. add the `<target directory>` to your system path so that the executables can be found

Usage
=====

### Command-line Usage

First, compile a Clafer model `model.cfr` into Clafer Python IR format as follows

```
clafer -m python model.cfr
```

This will produce `model.py` file in the same directory as the input `.cfr` file.

Next, execute

```
python Z3Run.py model.py
```

which will produce the AST in python and print the tree.

### Interactive Session Usage
In the interactive mode, the users can invoke the following commands...

Need help?
==========
* See [language's website](http://clafer.org) for news, technical reports and more
  * Check out a [Clafer tutorial](http://t3-necsis.cs.uwaterloo.ca:8091/Tutorial/Intro)
  * Try a live instance of [ClaferWiki](http://t3-necsis.cs.uwaterloo.ca:8091) which contains a repository of models for various applications
  * Try a live instance of [ClaferIDE](http://t3-necsis.cs.uwaterloo.ca:8094)
  * Try a live instance of [ClaferConfigurator](http://t3-necsis.cs.uwaterloo.ca:8093)
  * Try a live instance of [ClaferMooVisualizer](http://t3-necsis.cs.uwaterloo.ca:8092)
* Take a look at (incomplete) [Clafer by examples wiki](https://github.com/gsdlab/clafer/wiki)
* Browse example models in the [test suite](https://github.com/gsdlab/clafer/tree/master/test/positive) and [MOO examples](https://github.com/gsdlab/clafer/tree/master/spl_configurator/dataset)
* Post questions, report bugs, suggest improvements [GSD Lab Bug Tracker](http://gsd.uwaterloo.ca:8888/questions/). Tag your entries with `clafersmt` (so that we know what they are related to) and with `ezulkosk` or `michal` (so that Ed or Michał gets a notification).