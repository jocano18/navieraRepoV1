# Naviera Documentation Management System

Monorepo scaffold (Phase 1) for managing shipment documentation workflows: PDF extraction, digitization, validation, client notification, and approval.

**Stack:** Python 3.12 · FastAPI · React · TypeScript · Vite · PostgreSQL 16 · MailHog · Docker Compose

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- **Make** (opcional) o en Windows solo **`make.bat`** en la raíz del proyecto

## Quick start (3 comandos)

```bash
make up      # levanta todo (postgres, backend, frontend, mailhog)
make sync    # copia PDFs de backend/data/inbox al contenedor
make check   # comprueba que el API responde
```

**Windows sin Make** — desde la raíz del proyecto (`navieraV2`, donde está `docker-compose.yml`):

```powershell
# Recomendado en NAS (ruta \\servidor\...): PowerShell nativo
.\naviera.ps1 up
.\naviera.ps1 sync
.\naviera.ps1 check

# Alternativa: el .bat debe llevar .\ delante
.\make.bat up
.\make.bat sync
```

**Importante:** no uses `make up` ni `make.bat up` sin el `.\`. En rutas UNC del NAS, si `make.bat` falla con "no configuration file provided", usa **`.\naviera.ps1`**.

Abre http://localhost:5173 (Ctrl+F5 tras un rebuild).

Tras el build, **frontend (5173) y backend (8000)** arrancan en cuanto Postgres está listo.

### Windows + proyecto en NAS (`\\servidor\...`)

Docker Desktop **no puede montar** carpetas UNC. El `docker-compose.yml` usa volúmenes nombrados.

1. `make up` o `make.bat up`
2. `make sync` o `make.bat sync` — usa `pushd` para rutas `\\servidor\...`

En el **primer arranque**, el backend también copia PDFs embebidos en la imagen si el volumen inbox está vacío. Vuelve a ejecutar **sync** cuando agregues PDFs nuevos en `backend/data/inbox`.

Si el proyecto está en disco local (`C:\...`), puedes activar hot-reload con `docker-compose.override.example.yml` → `docker-compose.override.yml`.

### Service URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API docs (dev) | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |
| MailHog UI | http://localhost:8025 |
| PostgreSQL | localhost:5432 |

## Comandos (`make` o `make.bat`)

| Comando | Qué hace |
|---------|----------|
| `make help` | Lista todos los comandos |
| `make up` | Build + levanta todo en segundo plano |
| `make down` | Para y quita contenedores |
| `make restart` | `down` + `up` |
| `make rebuild` | Reconstruye imágenes y recrea contenedores |
| `make sync` | Sincroniza PDFs (`backend/data/inbox` → Docker) |
| `make status` | `docker compose ps` |
| `make check` | Health + inbox + prueba crear envío |
| `make logs` | Logs de backend y frontend |
| `make build` | Solo construye imágenes |
| `make install` | venv + npm en el host (opcional, para IDE) |
| `make test` | `pytest` en el contenedor backend |
| `make migrate` | `alembic upgrade head` |
| `make clean` | Limpia cachés Python |
| `make down-v` | Baja todo **y borra volúmenes** (reset BD/inbox) |
| `make up-fg` | Levanta en primer plano (logs en la misma ventana) |

## Project structure

```
naviera-docs/
├── backend/          # FastAPI + Clean Architecture
├── frontend/         # React + TypeScript + Vite
├── docs/             # architecture.md, state-machine.md
├── docker-compose.yml
├── Makefile
└── .env.example
```

See [docs/architecture.md](docs/architecture.md) for layer details and [docs/state-machine.md](docs/state-machine.md) for workflow states.

## Local development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Tests

```bash
cd backend
pytest tests -v
# or with Docker: make test
```

## License

Proprietary — Naviera project.
