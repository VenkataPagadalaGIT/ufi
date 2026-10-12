.PHONY: install test lint format typecheck example verify all

install:        ## editable install with dev extras
	pip install -e ".[dev]" ruff mypy pytest-cov

test:           ## run the test suite with coverage
	python -m pytest -q --cov=ufi --cov-report=term-missing

lint:           ## lint and format check
	ruff check src tests examples && ruff format --check src tests examples

format:         ## format in place
	ruff format src tests examples && ruff check --fix src tests examples

typecheck:      ## static types
	mypy src/ufi

example:        ## run the offline worked example
	cd examples/nanp && python make_demo_inputs.py && python build_example.py

verify:         ## confirm the released digests
	ufi verify examples/nanp/out/frozen_queries.json && ufi manifest examples/nanp/out/manifest.json

all: lint typecheck test example verify
