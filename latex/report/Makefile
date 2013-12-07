FILE    := smt_proposal
PICFIGS := $(patsubst %.pic,%.pic.tex,$(wildcard figs/*.pic))
SRCFIGS := $(wildcard figs/*.png)
FIGS    := $(patsubst %.png,%.eps,$(SRCFIGS))
ARGS	:= --shell-escape

all: $(FILE).tex *.bib figs
	pdflatex $(ARGS) $(FILE).tex || (rm $(FILE).pdf && false)
	bibtex $(FILE)
	pdflatex $(ARGS) $(FILE).tex 
	pdflatex $(ARGS) $(FILE).tex 
	 
#	dvipdfm -p letter -o $(FILE).pdf $(FILE) #Note, dvipdfm does not generate a IEEE-xplore compatible file by default
#	dvips -t letter -Ppdf -G0 $(FILE) -o $(FILE).ps
#	ps2pdf14 -dEmbedAllFonts=true -dUseFlateCompression=true -dPDFSETTINGS=/prepress $(FILE).ps

foo:
	echo $(SRCFIGS)
	echo $(FIGS)
	echo $(PICFIGS)

.PHONY: rubber

%.tex : %.pic.tex 
	pic -t tpicsmacros $< > $@

rubber: doc.tex
	rubber -o dvipdfm -v  doc.tex

figs: $(FIGS) $(PICFIGS)

%.eps : %.png
	/usr/bin/convert $< $@ 


%.eps : %.bmp
	/usr/bin/convert $< $@

%.pic.tex : %.pic
	pic -t tpicsmacros $< > $@


clean:
	rm -f *.aux *.bbl *.blg *.dvi *.idx *.log *.ilg *.ind *.out figs/*.pic.tex

