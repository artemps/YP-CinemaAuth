.PHONY: up
up:
	docker-compose -f docker-compose.dev.yml --env-file .env up --build -d && poetry run python src/main.py

.PHONY: test
test:
	cd src && poetry run pytest .

.PHONY: flakeheaven
flakeheaven:
	cd src && poetry run flakeheaven lint .

.PHONY: flake8
flake8:
	cd src && poetry run flake8 .

.PHONY: mypy
mypy:
	cd src && poetry run mypy .

.PHONY: isort
isort:
	cd src && poetry run isort .

.PHONY: lint
lint: flakeheaven flake8 mypy isort