install:  
	mkdir -p $(to)
	cp -f README.md $(to)/ClaferSMT-README.md
	cp -fr src $(to)
	cp -f claferSMT.sh $(to)	