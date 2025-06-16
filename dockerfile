FROM python:3.10-slim

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY pyproject.toml poetry.lock alembic.ini ./
COPY ./app ./app

RUN poetry install --no-root --without dev

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
