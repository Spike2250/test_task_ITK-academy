install:
	poetry install --no-root

start:
	poetry run python3 main.py

test:
	poetry run pytest

lint:
	poetry run flake8
