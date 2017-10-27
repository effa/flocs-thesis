.PHONY: all pdf watch clean open

all: pdf

pdf: thesis.tex
	latexmk -pdf -pv -pdflatex="pdflatex --shell-escape %O %S" thesis.tex

watch:
	latexmk -pdf -pvc -pdflatex="pdflatex --shell-escape %O %S" thesis.tex

clean:
	latexmk -CA

open:
	evince thesis.pdf &
