FILE?=ast.dot
ARG?=

all: 
	pip install -r requirements.txt
	python ./src/parse.py
	
dev:
	clear
	python ./src/parse.py -i ./tests/test_$(ARG).java -o src/javao -v -a

dev-g: dev
	dot -Tsvg src/javao.dot -o src/javao.svg
	xdg-open src/javao.svg

graph:
	dot -Tps $(FILE) -o src/ast.ps

vgraph:
	xdg-open src/ast.ps

build:
	gcc -c $(ARG).s -o $(ARG).o
	gcc -o $(ARG) -no-pie $(ARG).o
	./$(ARG)
	rm -f $(ARG).o $(ARG)

clean:
	rm -rf src/__pycache__
	rm -f src/parsetab.py src/parser.out src/parsetab.py src/*.dot src/*.ps ast* src/ast src/*.svg src/*.png src/*csv src/*.txt src/javao *.csv
	