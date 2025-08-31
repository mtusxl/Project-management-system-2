FROM python:3.12-slim AS builder
WORKDIR /app

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM python:3.12-slim AS runtime
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin


WORKDIR /app
COPY . .

CMD ["gunicorn", "--workers", "8", "--bind", "0.0.0.0:8000", "Project_Management_System.config.wsgi:application"]
