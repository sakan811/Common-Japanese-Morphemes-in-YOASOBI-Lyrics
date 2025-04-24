run:
	python main.py

visualize:
	python visualize.py

lint:
	ruff check . --fix --unsafe-fixes && ruff format .

test:
	pytest

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	docker-compose down --volumes --remove-orphans