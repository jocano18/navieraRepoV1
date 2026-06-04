# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    postgresql-client \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-spa \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --chown=appuser:appuser . .
# Copia PDFs al build (el volumen Docker monta encima de /app/data/inbox vacío al primer arranque)
COPY --chown=appuser:appuser data/inbox /app/inbox-seed

RUN mkdir -p /app/storage /app/data/inbox /app/data /app/inbox-seed \
    && chown -R appuser:appuser /app

USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --retries=3 --start-period=20s \
    CMD curl -f http://localhost:8000/health || exit 1

FROM runtime AS development

# runtime termina con USER appuser; hace falta root para sed en / y chown de volúmenes al arrancar.
USER root
COPY docker-entrypoint.dev.sh /docker-entrypoint.dev.sh
RUN sed -i 's/\r$//' /docker-entrypoint.dev.sh \
    && chmod +x /docker-entrypoint.dev.sh

ENTRYPOINT ["/docker-entrypoint.dev.sh"]

FROM runtime AS production

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
