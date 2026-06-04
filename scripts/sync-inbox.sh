#!/usr/bin/env bash
# Copia PDFs de backend/data/inbox al volumen Docker del backend.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INBOX="${ROOT}/backend/data/inbox"

if [[ ! -d "$INBOX" ]]; then
  echo "ERROR: No existe la carpeta: $INBOX" >&2
  exit 1
fi

if ! docker ps --filter 'name=naviera-backend' --filter 'status=running' -q | grep -q .; then
  echo "El contenedor naviera-backend no está en ejecución. Levanta primero:"
  echo "  docker compose up -d"
  exit 1
fi

echo "Copiando PDFs desde ${INBOX} ..."
docker cp "${INBOX}/." naviera-backend:/app/data/inbox/

count="$(find "$INBOX" -maxdepth 1 -name '*.pdf' 2>/dev/null | wc -l | tr -d ' ')"
echo "Listo. ${count} PDF(s) en el host."
echo "Verifica: curl -sf http://localhost:8000/inbox/pdfs"
