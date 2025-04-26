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

api-extract-morphemes:
	curl -X POST "http://localhost:8000/extract-morphemes/" \
		-H "Content-Type: application/json" 

api-visualize:
	curl -X POST "http://localhost:8000/visualize/" \
		-H "Content-Type: application/json" \
		-d '{"font_scale": 2.0}'

api: api-extract-morphemes api-visualize

app:
	fastapi run main.py