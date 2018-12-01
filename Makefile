# -*-  tab-width:4  -*-
# Define required macros here
SHELL = /bin/sh
FIGURES=figures/
RESULTS=results/
DATA=data/
FORMATS=png tiff pdf

.PHONY: clean png results docx

all: png pdf docx

docx:
	rm -rf bobcatsss-2019.docx
	pandoc -s bobcatsss-2019.md -o bobcatsss-2019.docx

pdf:
	rm -rf bobcatsss-2019.pdf
	pandoc -s bobcatsss-2019.md -o bobcatsss-2019.pdf

png:
	python ./scripts/main.py -t ${RESULTS} -i ${FIGURES} ${DATA}

results:
	python ./scripts/main.py -f ${FORMATS} -t ${RESULTS} -i ${FIGURES} ${DATA}

clean:
	rm -rf bobcatsss-2019.docx
	rm -rf bobcatsss-2019.pdf
	rm -rf ${FIGURES}
	rm -rf ${RESULTS}
