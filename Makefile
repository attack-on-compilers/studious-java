FILE?=ast.dot
OUTFILE=?ast.ps
ARG?=

all: clean
	python ./src/parse.py $(FILE) $(ARG) -o $(OUTFILE)

dev: clean
	clear
	python ./src/parse.py ./test/test1.java -o src/ast.dot

dev-g: dev
	dot -Tps src/ast.dot -o src/ast.ps
	xdg-open src/ast.ps

graph:
	dot -Tps $(FILE) -o $(OUTFILE)

vgraph:
	xdg-open $(FILE)

clean:
	rm -rf src/__pycache__
	rm -f src/parsetab.py src/parser.out src/parsetab.pyc src/*.dot src/*.ps src/ast
	