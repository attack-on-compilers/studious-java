FILE?=ast.dot
ARG?=

all: 
	pip install -r requirements.txt
	python ./src/parse.py
	
dev: clean
	clear
	python ./src/parse.py -i ./tests/test_5.java -o src/ast.dot -v -a

dev-g: dev
	dot -Tsvg src/ast.dot -o src/ast.svg
	xdg-open src/ast.svg

graph:
	dot -Tps $(FILE) -o src/ast.ps

vgraph:
	xdg-open src/ast.ps

clean:
	rm -rf src/__pycache__
	rm -f src/parsetab.py src/parser.out src/parsetab.py src/*.dot src/*.ps ast* src/ast src/*.svg src/*.png
	