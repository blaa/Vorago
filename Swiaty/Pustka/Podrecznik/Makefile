OBJECTS=Vorago.latex Style.latex Magic.latex SpellTable.latex Races.latex \
	Equipment.latex Development.latex
LATEX=pdflatex


# Easier way:

Vorago.pdf: ${OBJECTS}
	${LATEX} -file-line-error -halt-on-error Vorago.latex
	makeindex Vorago
	${LATEX} Vorago.latex
#	dvipdf Vorago.dvi

clean:
	rm -f *.dvi *.pdf *.log *.aux *.tex *.ilg *.ind

distclean: clean
	rm -f *.idx *.lot *.toc
