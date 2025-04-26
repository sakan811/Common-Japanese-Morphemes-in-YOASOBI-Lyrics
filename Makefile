main:
	python main.py

visualize:
	python visualize.py

run: main visualize

lint:
	ruff check . --fix --unsafe-fixes

format:
	ruff format .

mypy:
	mypy . --strict --ignore-missing-imports

qa: lint format mypy

test:
	python -m pytest

up:
	docker compose up -d

build:
	docker compose -f docker-compose-build.yml up -d --build

down:
	docker compose down

clean:
	docker compose down --volumes --remove-orphans