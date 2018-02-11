# Master Thesis on Adaptive Programming

This repository contains text, slides, analysis for master thesis on
*Adaptive System for Learning Programming*.

## Mission

Make learning introductory programming efficient using artificial intelligence.

## Goals

1. Create an overview of existing systems for learning introductory programming
   and related research on adaptlive learning systems
   (domain and student models, tutoring techniques, user interface,
   adaptive learning system architecutre, and evaluation of all these components).
2. Create an online system for learning introductory programming containing at least 100 tasks,
   that will be used by at least 50 users per day.
3. The system collects data about students' interactions
   and reports metrics that help to detect issues with the content or system behavior.
4. Using both simulated and collected data, evaluate delpoyed models,
   techniques, and the complete system, as well as several alternative models and techniques.
5. Based on both the analyses and user testing at schools,
   formulate recommendations for iterative improvement of our system and for
   adaptive learning systems for introductory programming in general.


## Text

TODO: link to the last generated PDF.

To write the text, you can you prepared make commands (assuming latexmk installed):
```
make pdf  # one time compilation
make watch  # continuous mode (compile automatically on change)
```

You can edit your latexmk settings in `~/.latexmkrc`:
```
$pdf_previewer = 'start evince';
$clean_ext = 'synctex.gz run.xml tex.bak bbl bcf fdb_latexmk run tdo %R-blx.bib'
```

## Slides

TODO: link to the last generated slides.

TODO: how to edit slides

## Analysis

To reproduce analyses, create virtual environment with Python 3.5 and listed dependencies.
For example, if using virtualenvwrapper:

```
mkvirtualenv -a . thesis
make install
```

Then open and run prepared jupyter notebooks:
```
workon thesis
jupyter notebook
```

## RoboMission

The developed learning system: <https://en.robomise.cz>.

Source code: <https://github.com/adaptive-learning/robomission>.
