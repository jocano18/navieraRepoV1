#!/bin/sh
set -e

cd /app

if [ ! -d node_modules ] || [ ! -f node_modules/.install-stamp ]; then
  echo "[frontend] Installing npm dependencies..."
  if [ -f package-lock.json ]; then
    npm ci
  else
    npm install
  fi
  touch node_modules/.install-stamp
fi

export VITE_PROXY_TARGET="${VITE_PROXY_TARGET:-http://backend:8000}"
echo "[frontend] Starting Vite on :5173 (API proxy -> ${VITE_PROXY_TARGET})"
exec npm run dev
