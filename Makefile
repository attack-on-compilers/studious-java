FILE?=ast.dot
ARG?=

all: 
	pip install -r requirements.txt
	python ./src/parse.py
	
dev: clean
	clear
	python ./src/parse.py ./test/test1.java -o src/ast.dot

dev-g: dev
	dot -Tps src/ast.dot -o src/ast.ps
	xdg-open src/ast.ps

graph:
	dot -Tps $(FILE) -o src/ast.ps

vgraph:
	xdg-open src/ast.ps

clean:
	cd milestone1
	rm -rf src/__pycache__
	rm -f src/parsetab.py src/parser.out src/parsetab.py src/*.dot src/*.ps ast*
	