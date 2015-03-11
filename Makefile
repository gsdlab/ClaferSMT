SRC_DIR  := src

all:
	# Create the Egg
	$(MAKE) -C $(SRC_DIR)

init:
	# Copy Z3
	@if [ -z $(z3bin) ]; then \
		echo "Provide the path to Z3 SMT solver's bin (or build) folder to 'z3bin' flag";  \
		read z3bin; \
	fi
	cp -f $(z3bin)/*.py* src
	# Windows Z3
	cp -f $(z3bin)/libz3.dll .  2>/dev/null || :    # supress error message and exit code if missing
	# Linux Z3
	cp -f $(z3bin)/libz3.so .   2>/dev/null || :
	# Mac Z3
	cp -f $(z3bin)/libz3.dylib .  2>/dev/null || :

install:
	mkdir -p $(to)
	cp -f README.md $(to)/ClaferSMT-README.md
	cp -f ClaferSMT.egg $(to)
	# Windows Z3
	cp -f libz3.dll $(to)  2>/dev/null || :
	# Linux Z3
	cp -f libz3.so $(to)  2>/dev/null || :
	# Mac Z3
	cp -f libz3.dylib $(to)  2>/dev/null || :
	cp claferSMT.sh $(to)

clean:
	find . -type d -name '__pycache__' -print0 | xargs -0 rm -fr
	find . -type f -name '*.pyo' -print0 | xargs -0 rm -f
	find . -type f -name '*.pyc' -print0 | xargs -0 rm -f
