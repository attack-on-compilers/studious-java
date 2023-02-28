FILE?=ast.dot
OUTFILE=?ast.ps
ARG?=

all:
	python ./src/parse.py $(FILE) $(ARG) -o $(OUTFILE)

test: clean
	python ./src/parse.py ./test/test_1.java -o src/ast.dot
	python ./src/parse.py ./test/test_2.java -o src/ast.dot
	python ./src/parse.py ./test/test_3.java -o src/ast.dot
	python ./src/parse.py ./test/test_4.java -o src/ast.dot
	python ./src/parse.py ./test/test_5.java -o src/ast.dot
	python ./src/parse.py ./test/test_6.java -o src/ast.dot
	python ./src/parse.py ./test/test_7.java -o src/ast.dot
	python ./src/parse.py ./test/test_8.java -o src/ast.dot



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
	