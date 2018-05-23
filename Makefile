.PHONY: all pdf watch clean open install notebook slides

# Text.
# Assuming latexmk and evince installed.

all: pdf

pdf: thesis.tex
	latexmk -pdf -pv -pdflatex="pdflatex -interaction=nonstopmode -halt-on-error -quiet --shell-escape %O %S" thesis.tex

watch:
	latexmk -pdf -pvc -pdflatex="pdflatex -interaction=nonstopmode -quiet --shell-escape %O %S" thesis.tex

clean:
	latexmk -CA

open:
	evince thesis.pdf &

# Slides.
slides: slides/slides.tex
	cd slides; latexmk -pdf -pv -pdflatex="pdflatex -interaction batchmode --shell-escape %O %S" slides.tex

slides-watch:
	cd slides; latexmk -pdf -pvc -pdflatex="pdflatex -interaction=nonstopmode -quiet --shell-escape %O %S" slides.tex

# Analysis.
# Recommended to run inside a virtual environment (see README).

install:
	pip install -r requirements.txt
	jupyter nbextension enable --py widgetsnbextension --sys-prefix

notebook:
	jupyter notebook
