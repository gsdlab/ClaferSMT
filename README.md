ClaferSMT
=========

v0.3.6.2

Instance generator and multi-objective optimizer based on SMT solvers (currently Microsoft Z3) for Clafer.

Contributors
------------

* [Ed Zulkoski](http://gsd.uwaterloo.ca/ezulkosk). Main developer.
* [Rafael Olaechea](http://gsd.uwaterloo.ca/rolaechea). Developer.
* [Alexandr Murashkin](http://gsd.uwaterloo.ca/amurashk). Testing.
* [Michał Antkiewicz](http://gsd.uwaterloo.ca/mantkiew). Testing, technology transfer.

Getting the Clafer SMT Backend
------------------------------

### Dependencies for running

Regardless of the installation method, the following are required:

* [Python 3](https://www.python.org/download/releases/3.4.1/) v3.4.1
* [Clafer Compiler](https://github.com/gsdlab/clafer) v0.3.6.1
  * Required for compiling Clafer files (`.cfr`) into the Clafer Python IR format (`.py`), so that they can be run using the tool.

### Installation from binaries

Binary distributions of the release 0.3.6.1 of Clafer Tools for Windows, Mac, and Linux, 
can be downloaded from [Clafer Tools - Binary Distributions](http://http://gsd.uwaterloo.ca/clafer-tools-binary-distributions). 

1. download the binaries and unpack `<target directory>` of your choice
2. add the `<target directory>` to your system path so that the executables can be found

### Installation from source code

Dependencies

* [Z3 SMT Solver](http://z3.codeplex.com/) v4.2.3
  * install to `<z3 install directory>` of your choice
* [bintrees](https://bitbucket.org/mozman/bintrees)
  * pip install bintrees (make sure it is installed for Python 3).
  * (optional): Remove the warning messages from bintrees' imports.

1. install the dependencies
2. open the command line terminal. On Windows, open MinGW.
3. in some `<source directory>` of your choice, execute 
  * `git clone git://github.com/gsdlab/ClaferSMT.git`
4. in `<source directory>/ClaferSMT`, execute
  * `make init z3bin=<z3 install directory>/bin`
  * `make` - this will produce `ClaferSMT.egg`, which contains Z3.
  * `make install to=<target directory>`

Usage
=====

### Command-line Usage

First, compile a Clafer model `model.cfr` into Clafer Python IR format as follows

```
clafer -m python model.cfr
```

This will produce `model.py` file in the same directory as the input `.cfr` file.

Next, either execute

```
./claferSMT.sh model.py
```

when using source code, or 

```
python claferSMT.egg model.py
```

when using the egg.

Help printed by `--help`

```
$ python claferSMT.egg --help
usage: claferSMT.egg [-h]
                     [--mode {experiment,modelstats,normal,debug,test,one,repl,all}]
                     [--printconstraints] [--profiling] [--cprofiling]
                     [--numinstances NUMINSTANCES] [--globalscope GLOBALSCOPE]
                     [--testset TEST_SET] [--stringconstraints]
                     [--solver {z3,cvc4,smt2}] [--printuniquenames]
                     [--showinheritance] [--version] [--delimeter DELIMETER]
                     [--indentation {doublespace,tab}] [--magnifyingglass]
                     [--produceunsatcore] [--usebitvectors] [--cores CORES]
                     [--server SERVER] [--service SERVICE]
                     [--split {no_split,random_optional_clafer_toggle,random_xor_gcard_clafer_toggle,top_optional_clafer_toggle,biggest_range_split,divide_biggest_ranges_in_two,smallest_range_split,bottom_optional_clafer_toggle,random_range_split,NO_SPLIT}]
                     [--numsplit NUMSPLIT] [--heuristicsfile HEURISTICS_FILE]
                     [--experimentnumsplits [EXPERIMENTNUMSPLITS [EXPERIMENTNUMSPLITS ...]]]
                     [--modelclass {featuremodel}]
                     [--classifier {ldac,svm,classtree}]
                     [--learningiterations LEARNING_ITERATIONS]
                     [--timeout TIME_OUT]
                     [file]

Process a clafer model with Z3.

positional arguments:
  file                  the clafer python file

optional arguments:
  -h, --help            show this help message and exit
  --mode {experiment,modelstats,normal,debug,test,one,repl,all}, -m {experiment,modelstats,normal,debug,test,one,repl,all}
  --printconstraints, --pc
                        print all Z3 constraints (for debugging)
  --profiling, -p       basic profiling of phases of the solver
  --cprofiling          uses cprofile for profiling functions of the
                        translation
  --numinstances NUMINSTANCES, -n NUMINSTANCES
                        the number of models to be displayed (-1 for all)
  --globalscope GLOBALSCOPE, -g GLOBALSCOPE
                        the global scope for unbounded clafers (note that this
                        does not match regular clafer)
  --testset TEST_SET, -t TEST_SET
                        The test set to be used for modes [experiment | test |
                        one | all], or the number of tests to generate
  --stringconstraints, -s
                        Flag to output to Z3-Str format instead
  --solver {z3,cvc4,smt2}
                        Backend solver
  --printuniquenames, -u
                        Print clafers with unique prefixes
  --showinheritance     Show super-clafers explicitly
  --version, -v         Print version number.
  --delimeter DELIMETER
                        Delimeter between instances.
  --indentation {doublespace,tab}
  --magnifyingglass     Print equally optimal solutions if optimizing
  --produceunsatcore    produce unsat core for UNSAT specifications
  --usebitvectors       Use bitvectors to represent clafer instances
  --cores CORES, -c CORES
                        the number of cores for parallel processing
  --server SERVER       The name of the Server clafer in SAP problems (used
                        for parallelization)
  --service SERVICE     The name of the Service clafer in SAP problems (used
                        for parallelization)
  --split {no_split,random_optional_clafer_toggle,random_xor_gcard_clafer_toggle,top_optional_clafer_toggle,biggest_range_split,divide_biggest_ranges_in_two,smallest_range_split,bottom_optional_clafer_toggle,random_range_split,NO_SPLIT}
  --numsplit NUMSPLIT   The number of splits to perform (default = #cores)
  --heuristicsfile HEURISTICS_FILE
                        File containing the heuristics to be tested. If none
                        given, all will be used
  --experimentnumsplits [EXPERIMENTNUMSPLITS [EXPERIMENTNUMSPLITS ...]]
                        List of the number of splits to perform (default =
                        #cores)
  --modelclass {featuremodel}
  --classifier {ldac,svm,classtree}
                        The learning technique to be applied
  --learningiterations LEARNING_ITERATIONS
                        the number of iterations through the learning process
  --timeout TIME_OUT    The time out for consumers
```

### Interactive Session Usage

To run ClaferSMT in an interactive mode use the parameter `--mode=repl`.

In the interactive mode, the users can invoke the following commands:

```
ClaferZ3 > h
n -- get next model
r -- reset
i [num] -- increase (or decrease) the global scope by num (default=+1)
s num -- set scope to num
h -- help
q -- quit
```

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