POETRY := $(shell command -v poetry 2> /dev/null)

.PHONY: up
up:
	docker-compose -f docker-compose.dev.yml --env-file .env up --build -d && $(POETRY) run python src/main.py

.PHONY: test
test:
	$(POETRY) run pytest src/

.PHONY: ruff
ruff:
	$(POETRY) run ruff check src/

.PHONY: mypy
mypy:
	$(POETRY) run mypy src/

.PHONY: lint
lint: ruff mypy