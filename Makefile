.PHONY: up
up:
	docker-compose -f docker-compose.dev.yml --env-file .env up --build -d && poetry run python src/main.py

.PHONY: test
test:
	cd src && poetry run pytest ./

.PHONY: ruff
ruff:
	cd src && poetry run ruff check ./

.PHONY: mypy
mypy:
	cd src && poetry run mypy ./

.PHONY: lint
lint: ruff mypy