.PHONY: all pdf watch clean open

all: pdf

pdf: thesis.tex
	latexmk -pdf -pv thesis.tex

watch:
	latexmk -pdf -pvc thesis.tex

clean:
	latexmk -CA

open:
	evince thesis.pdf &
