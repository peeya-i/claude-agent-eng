.PHONY: install install-dev run test lint evals

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

run:
	python -m class_02.main

test:
	pytest --cov=src/class_02

lint:
	ruff check src tests evals

evals:
	python -m evals.run_evals
