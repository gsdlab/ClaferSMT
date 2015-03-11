ClaferSMT
=========

v0.3.9

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

* [Python 3](https://www.python.org/downloads/) v3.4.*
* [Clafer Compiler](https://github.com/gsdlab/clafer) v0.3.9
  * Required for compiling Clafer files (`.cfr`) into the Clafer Python IR format (`.py`), so that they can be run using the tool.
* [Z3 SMT Solver](http://z3.codeplex.com/) v4.3.2.9d221c037a95
  * included in the binary distribution

### Installation from binaries

Binary distributions of the release 0.3.9 of Clafer Tools for Windows, Mac, and Linux, 
can be downloaded from [Clafer Tools - Binary Distributions](http://http://gsd.uwaterloo.ca/clafer-tools-binary-distributions). 

1. download the binaries and unpack `<target directory>` of your choice
2. add the `<target directory>` to your system path so that the executables can be found
3. on Linux, add the `<target directory>` to the `LD_LIBRARY_PATH`
4. on Mac, add the `<target directory>` to the `DYLD_LIBRARY_PATH`
5. alternatively, you can modify the `CLAFER_SMT` variable to point to the `<target directory>` in the script `claferSMT.sh`

### Installation from source code

Dependencies

* Z3 SMT Solver v4.3.2.4ea3ed7e273a
  * [Z3 for Windows](https://z3.codeplex.com/downloads/get/918997) x86
  * [Z3 for Ubuntu](https://z3.codeplex.com/downloads/get/918996) x64
  * [Z3 for OS X](https://z3.codeplex.com/downloads/get/918993) x64
  * this particular version has been tested. The latest one from Oct 24, 2014 does not work.
  * unzip to `<z3 install directory>` of your choice

1. install the dependencies
2. open the command line terminal. On Windows, open MinGW/MSYS.
3. in some `<source directory>` of your choice, execute 
  * `git clone git://github.com/gsdlab/ClaferSMT.git`
4. in `<source directory>/ClaferSMT`, execute
  * `make init z3bin=<z3 install directory>/bin`
  * `make` - this will produce `ClaferSMT.egg`, which contains Z3.
  * `make install to=<target directory>`
5. on Linux, add the `<target directory>` to the `LD_LIBRARY_PATH`
6. on Mac, add the `<target directory>` to the `DYLD_LIBRARY_PATH`
7. alternatively, you can modify the `CLAFER_SMT` variable to point to the `<target directory>` in the script `claferSMT.sh`

Integration with Sublime Text 2/3
-------------------------------

See [ClaferToolsST](https://github.com/gsdlab/ClaferToolsST)

Usage
=====

### Command-line Usage

ClaferSMT can be used directly from source code using the script `claferSMTsrc.sh` (only included in source code).
From binary distribution:

* On Linux: `./claferSMT.sh <model[.cfr|.py]> <options>`
  * the script sets the `LD_LIBRARY_PATH` to `pwd` so that the `libz3.so` can be located
* On Windows: `python ClaferSMT.egg <model[.cfr|.py]> <options>` or the same as on Linux
  * should be executed in the same folder as the `libz3.dll` so that it can be found
* On Mac: `./claferSMT.sh <model[.cfr|.py]> <options>` or the same as on Linux
  * should be executed in the same folder as the `libz3.dylib` so that it can be found

NOTE: when giving a `.cfr` model as argument, the Clafer compiler executable must be in the PATH because it's called to produce the `.py` file.

Help printed by `--help`

```
$ python ClaferSMT.egg --help
usage: ClaferSMT.egg [-h]
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
ClaferSMT > h
n -- get next model
r -- reset
i [num] -- increase (or decrease) the global scope by num (default=+1)
s num -- set scope to num
h -- help
q -- quit
```

Need help?
==========
* Visit [language's website](http://clafer.org).
* Report issues to [issue tracker](https://github.com/gsdlab/ClaferSMT/issues)
