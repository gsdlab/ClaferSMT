ifeq ($(OS),Windows_NT)
	PYTHON3 := python
else
	PYTHON3 := python3
endif

all:
	# Create the Egg
	rm -f ../ClaferSMT.egg
	$(PYTHON3) -m compileall .
	zip -r9 ../ClaferSMT.egg . -x Makefile