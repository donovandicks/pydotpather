.PHONY: all test clean

SHELL := /bin/bash

TEST_DEPS = tox pytest pytest-sugar pytest-benchmark pytest-examples
DEV_DEPS = wheel black ruff

clean:
	@rm -rf ./venv
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' | xargs rm -rf
	@find . -type d -name '*.ropeproject' | xargs rm -rf
	@rm -rf build/
	@rm -rf dist/
	@rm -rf src/*.egg*
	@rm -f MANIFEST
	@rm -rf docs/build/
	@rm -f .coverage.*

init:
	python3 -m venv venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install $(DEV_DEPS) $(TEST_DEPS)

install:
	./venv/bin/pip install .

lint:
	black --check .
	ruff check --config pyproject.toml src/

fmt:
	black .

dev-deps:
	./venv/bin/pip install -U $(DEV_DEPS) $(TEST_DEPS)

test:
	tox run-parallel -p all

test-examples:
	pytest -m "examples" .

bench:
	pytest -m "benchmarks" .
