# Naviera Docs — Backend

University-grade **Clean Architecture** backend for shipping documentation management: inbox PDF scanning, extraction (native + OCR), digitization, comparison, state machine workflow, and client notification.

## Quick start

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate  |  Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # optional — defaults use SQLite + ./data/inbox

# Drop B/L PDFs into data/inbox/
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs

Default client UUID (seeded): `00000000-0000-0000-0000-000000000001`

## Docker (from repo root)

```bash
docker compose up --build
```

Backend mounts `backend/data/inbox` and uses SQLite at `backend/data/naviera.db` by default.

## Tests

```bash
pytest tests -v
```

## Database

- **Default:** `sqlite+aiosqlite:///./data/naviera.db`
- **PostgreSQL:** set `DATABASE_URL=postgresql+asyncpg://...` and `DATABASE_URL_SYNC=postgresql://...`

```bash
alembic upgrade head
```

Tables are also auto-created on startup for local dev.

## PDF extraction architecture

1. **Text layer detection** (PyMuPDF) → pdfplumber if native, else **Tesseract OCR** (pdf2image + poppler).
2. **CarrierDetector** inspects text → **ExtractorFactory** picks strategy.
3. **GenericBlExtractor** — regex/label parser for canonical fields.
4. **AmassExtractor** — example carrier-specific strategy (extends generic).

### Adding a new carrier extractor

1. Create `app/infrastructure/pdf/carriers/your_carrier_extractor.py` subclassing `GenericBlExtractor`.
2. Register in `ExtractorFactory._strategies`.
3. Add keyword in `CarrierDetector._CARRIER_KEYWORDS`.

No use case or API changes required (Open/Closed).

## API overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/inbox/pdfs` | List inbox PDFs |
| POST | `/shipments` | Create shipment from inbox file |
| POST | `/shipments/{id}/extract` | Extract B/L fields |
| GET | `/shipments/{id}/pdf` | Stream PDF (`application/pdf`) |
| POST | `/shipments/{id}/digitized-data` | Register typed data |
| GET | `/shipments/{id}/comparison` | Field diff |
| PATCH | `/shipments/{id}/digitized-data` | Correct data |
| POST | `/shipments/{id}/validate` | Executive validation |
| POST | `/shipments/{id}/approve` | Notify client (email includes approve button) |
| GET | `/public/approve?token=…` | Client email link → approve + finalize |
| POST | `/shipments/{id}/client-approve` | Client approval (manual / API) |
| POST | `/shipments/{id}/finalize` | Finalize |
| POST | `/shipments/{id}/novelty` | Register novelty |

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | SQLite async URL | SQLAlchemy async connection |
| `INBOX_PATH` | `./data/inbox` | Incoming B/L folder |
| `STORAGE_LOCAL_PATH` | `./storage` | Stored shipment PDFs |
| `USE_CONSOLE_NOTIFIER` | `true` | Log emails instead of SMTP |
| `SMTP_HOST` | `mailhog` | SMTP when console notifier disabled |
| `PUBLIC_API_URL` | `http://localhost:8000` | Base URL for approve button in emails |
| `APPROVAL_TOKEN_SECRET` | (dev default) | HMAC secret for email approval links |
| `APPROVAL_TOKEN_MAX_AGE_DAYS` | `7` | Link expiration |

## Project layout

```
app/domain/          # Entities, value objects, state machine (no third-party imports)
app/application/     # Use cases + ports
app/infrastructure/  # PDF, SQLAlchemy, email, storage adapters
app/interfaces/      # FastAPI routers, schemas, DI
tests/               # Unit + integration (httpx AsyncClient)
```

## System dependencies (Docker includes these)

- `tesseract-ocr` + `tesseract-ocr-eng`
- `poppler-utils` (for pdf2image)
