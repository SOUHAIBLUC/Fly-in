.PHONY: install run debug clean lint lint-strict

install:
	python -m pip install --upgrade pip
	@if [ -f requirements.txt ]; then \
		python -m pip install -r requirements.txt; \
	else \
		python -m pip install flake8 mypy; \
	fi

run:
	python main.py map.txt

debug:
	python -m pdb main.py

clean:
	-find . -type d -name "__pycache__" -exec rm -rf {} + || true
	-rm -rf .mypy_cache .pytest_cache *.pyc

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
