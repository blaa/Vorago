OBJECTS=Vorago.latex Chapter1.latex Chapter2.latex Chapter3.latex Style.latex 
LATEX=pdflatex

.PHONY: Vorago.pdf
# Easier way:

Vorago.pdf: ${OBJECTS}
	${LATEX} -file-line-error -halt-on-error Screen.latex
	makeindex Screen
	${LATEX} Screen.latex
	mv Screen.pdf Vorago.pdf

Vorago_Book.pdf: ${OBJECTS}
	${LATEX} -output-format=dvi -file-line-error -halt-on-error Print.latex
	makeindex Print
	${LATEX} -output-format=dvi Print.latex
	dvibook Print.dvi > Print2.dvi
	dvipdf Print2.dvi
	mv Print2.pdf Vorago_Book.pdf
	rm -f Print.dvi Print2.dvi

clean:
	rm -f *.dvi *.pdf *.log *.aux *.tex *.ilg *.ind

distclean: clean
	rm -f *.idx *.lot *.toc
