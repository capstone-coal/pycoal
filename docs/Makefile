all : report.pdf problem-statement.pdf requirements.pdf techreview.pdf design.pdf \
presentation.pdf problem-statement-student.pdf fall-report.pdf

# execute pdflatex twice to update references

report.pdf :
	pdflatex report.ltx
	pdflatex report.ltx

problem-statement.pdf :
	pdflatex problem-statement.ltx
	pdflatex problem-statement.ltx

requirements.pdf :
	pdflatex requirements.ltx
	pdflatex requirements.ltx

techreview.pdf :
	pdflatex techreview.ltx
	pdflatex techreview.ltx

design.pdf :
	pdflatex design.ltx
	pdflatex design.ltx

presentation.pdf :
	pdflatex presentation.ltx
	pdflatex presentation.ltx

presentation-winter.pdf :
	pdflatex presentation-winter.ltx
	pdflatex presentation-winter.ltx

problem-statement-student.pdf :
	pdflatex problem-statement-student.ltx
	pdflatex problem-statement-student.ltx

fall-report.pdf :
	pdflatex fall-report.ltx
	pdflatex fall-report.ltx

clean :
	rm -f report.pdf
	rm -f problem-statement.pdf
	rm -f requirements.pdf
#	rm -f techreview.pdf
	rm -f design.pdf
	rm -f presentation.pdf
	rm -f problem-statement-student.pdf
	rm -f fall-report.pdf
