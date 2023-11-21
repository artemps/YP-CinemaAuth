# CinemaAuth

## Сервис авторизации пользователей

**Перед первым запуском установите poetry, затем зависимости**
```shell
poetry install
```

**Ручной запуск**
```shell
docker-compose up -d
poetry run python src/main.py
```

**Автоматический запуск**
```shell
make up
```

**Для запуска тестов**
```shell
make test
```

**Для запуска линтеров**
```shell
make lint
```
