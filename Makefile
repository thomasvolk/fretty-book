all: test

FRETTY_BOOK=python -m fretty_book

test:
	mkdir -p out
	@echo "check help ..."
	$(FRETTY_BOOK) -v
	$(FRETTY_BOOK) -h
	$(FRETTY_BOOK) --embed example/simple.html
	@echo "process documents ..."
	$(FRETTY_BOOK) -V example/simple.html -o out/simple.html
	diff out/simple.html example/simple/simple.html
	test -f out/fretty-0.svg
	mkdir -p out/html
	$(FRETTY_BOOK) -V example/document.html -o out/html/document.html
	mkdir -p out/html-embed
	$(FRETTY_BOOK) -V --embed example/document.html -o out/html-embed/document.html
	mkdir -p out/html-png
	$(FRETTY_BOOK) -V --png example/document.html -o out/html-png/document.html
	mkdir -p out/xhtml
	$(FRETTY_BOOK) -V example/document.xhtml -o out/xhtml/document.xhtml
	mkdir -p out/xhtml-png
	$(FRETTY_BOOK) -V --png example/document.xhtml -o out/xhtml-png/document.xhtml
	mkdir -p out/xhtml-embed
	$(FRETTY_BOOK) -V --embed example/document.xhtml -o out/xhtml-embed/document.xhtml

build: test
	pip install build
	python -m build --wheel

install:
	pip install -r requirements.txt
	python -m pip install -e .

upload: build
	pip install twine
	PYTHONIOENCODING=utf-8 twine upload --repository pypi dist/*

upload-test: build
	pip install twine
	PYTHONIOENCODING=utf-8 twine upload --repository testpypi dist/*

clean:
	rm -rf out build dist *.egg-info venv

