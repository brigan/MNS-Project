ALL: report.pdf slides.pdf

report.pdf: report.tex
	pdflatex report && bibtex report && pdflatex report && pdflatex report

#figures/*pdf:
#	for F in images/*eps; do epstopdf $$F; done

slides.pdf: slides.tex
	pdflatex slides
	rm -rf slides.toc slides.aux slides.log slides.snm slides.nav slides.out

clean:
	rm -rf report.toc report.aux report.log report.bbl report.blg report.out report.pdf slides.pdf graphics/*pdf
