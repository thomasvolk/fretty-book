all: test

PYTHON=./venv/bin/python3
FRETTY_BOOK=./venv/bin/fretty-book
TWINE=./venv/bin/twine


venv:
	python3 -m venv venv
	$(PYTHON) -m pip install fretty[PNG]
	$(PYTHON) -m pip install build
	$(PYTHON) -m pip install twine
	

$(FRETTY_BOOK): venv
	$(PYTHON) -m pip install -e .

test: $(FRETTY_BOOK)
	mkdir -p out
	@echo "check help ..."
	$(FRETTY_BOOK) -v
	$(FRETTY_BOOK) -h
	@echo "process documents ..."
	mkdir -p out/html
	$(FRETTY_BOOK) example/document.html -o out/html/document.html
	mkdir -p out/xhtml
	$(FRETTY_BOOK) example/document.xhtml -o out/html/document.xhtml

build: test
	$(PYTHON) -m build --wheel

upload: build
	PYTHONIOENCODING=utf-8 $(TWINE) upload --repository pypi dist/*

upload-test: build
	PYTHONIOENCODING=utf-8 $(TWINE) upload --repository testpypi dist/*

clean:
	rm -rf out build dist *.egg-info venv

