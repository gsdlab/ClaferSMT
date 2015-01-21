ifeq ($(OS),Windows_NT)
	PYTHON3 := python
else
	PYTHON3 := python3
endif

all:
	# Create the Egg
	rm -f ../egg
	$(PYTHON3) -m compileall .
	zip -r9 ../egg . -x Makefile