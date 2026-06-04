#!/bin/sh
set -e

# Los volúmenes nombrados de Docker suelen crearse como root; la API corre como appuser.
mkdir -p /app/storage/shipments /app/data/inbox
chown -R appuser:appuser /app/storage /app/data

run_appuser() {
  su -s /bin/sh appuser -c "$*"
}

echo "[backend] Waiting for PostgreSQL..."
until pg_isready -h postgres -p 5432 -U naviera -d naviera >/dev/null 2>&1; do
  sleep 1
done
echo "[backend] PostgreSQL is ready."

echo "[backend] Applying migrations (if any)..."
run_appuser "alembic upgrade head" || echo "[backend] Alembic skipped (tables may already exist)."

echo "[backend] Seeding default client..."
run_appuser "python -c \"
import asyncio
from app.infrastructure.persistence.session import get_session_factory
from app.infrastructure.persistence.seed import seed_default_client

async def main() -> None:
    factory = get_session_factory()
    async with factory() as session:
        await seed_default_client(session)

asyncio.run(main())
\"" || echo "[backend] Seed skipped."

# Volumen inbox_data empieza vacío; copiar PDFs embebidos en la imagen
if [ -d /app/inbox-seed ] && [ -n "$(ls -A /app/inbox-seed 2>/dev/null)" ]; then
  if [ -z "$(ls -A /app/data/inbox 2>/dev/null)" ]; then
    echo "[backend] Seeding inbox from image..."
    run_appuser "cp -a /app/inbox-seed/. /app/data/inbox/"
  fi
fi

echo "[backend] Starting API on :8000"
# Sin --reload en Docker: el codigo va en la imagen, no en bind mount (NAS/UNC).
exec su -s /bin/sh appuser -c "exec uvicorn app.main:app --host 0.0.0.0 --port 8000"
