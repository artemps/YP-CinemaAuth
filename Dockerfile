FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock /opt/

WORKDIR /opt/

RUN  pip install --upgrade pip \
     && pip install poetry \
     && poetry config virtualenvs.create false \
     && poetry install --no-dev --no-interaction --no-ansi

COPY src/ /opt/app/

WORKDIR /opt/app/

EXPOSE 8080

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]