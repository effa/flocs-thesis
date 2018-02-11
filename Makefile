.PHONY: all pdf watch clean open install notebook

# Text.
# Assuming latexmk and evince installed.

all: pdf

pdf: thesis.tex
	latexmk -pdf -pv -pdflatex="pdflatex --shell-escape %O %S" thesis.tex

watch:
	latexmk -pdf -pvc -pdflatex="pdflatex --shell-escape %O %S" thesis.tex

clean:
	latexmk -CA

open:
	evince thesis.pdf &

# Analysis.
# Recommended to run inside a virtual environment (see README).

install:
	pip install -r requirements.txt
	jupyter nbextension enable --py widgetsnbextension --sys-prefix

notebook:
	jupyter notebook
