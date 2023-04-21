FILE?=ast.dot
ARG?=

all: 
	pip install -r requirements.txt
	clear
	python ./src/main.py -i ./tests/test_$(ARG).java -o src/javao
	make build ARG=output
	
dev:
	clear
	python ./src/main.py -i ./tests/test_$(ARG).java -o src/javao -v -a
	make build ARG=output
	

dev-g: dev
	dot -Tsvg src/javao.dot -o src/javao.svg
	xdg-open src/javao.svg

graph:
	dot -Tsvg src/javao.dot -o src/javao.svg
	xdg-open src/javao.svg

vgraph:
	xdg-open src/ast.ps

build:
	gcc -c $(ARG).s -o $(ARG).o; gcc -o $(ARG) -no-pie $(ARG).o; ./$(ARG); rm -f $(ARG).o $(ARG)

clean:
	rm -rf src/__pycache__
	rm -f src/parsetab.py src/parser.out src/parsetab.py src/*.dot src/*.ps ast* src/ast src/*.svg src/*.png src/*csv src/*.txt src/javao *.csv
	