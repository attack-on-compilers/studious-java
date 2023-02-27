all:
	python ./src/parse.py ./test/test1.java

clean:
	rm -rf src/parsetab.py src/parser.out src/parsetab.pyc src/__pycache__
