all:
	./src/lex.py ./test/test1.java

clean:
	rm -f src/parsetab.py src/parser.out src/parsetab.pyc
