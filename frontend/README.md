# Naviera Docs — Frontend

React 19 + TypeScript + Vite frontend for the Bill of Lading documentation workflow. Consumes the FastAPI backend with a feature-based architecture and Naviera brand design system.

## Quick start

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). Ensure the backend runs at the URL in `VITE_API_URL` (default `http://localhost:8000`).

## Environment variables

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | FastAPI base URL (preferred) |
| `VITE_API_BASE_URL` | Legacy alias used by docker-compose |

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Vite dev server |
| `npm run build` | Production build |
| `npm run lint` | ESLint (includes feature boundaries) |
| `npm run typecheck` | `tsc --noEmit` |
| `npm test` | Vitest + RTL + MSW |

## Docker

```bash
# Development (hot reload)
docker build --target development -t naviera-frontend-dev .
docker run -p 5173:5173 -e VITE_API_URL=http://host.docker.internal:8000 naviera-frontend-dev

# Production (nginx)
docker build --target production -t naviera-frontend .
docker run -p 8080:80 naviera-frontend
```

From the repo root, `docker compose up` starts frontend + backend together.

## Estructura de `src/` (activa)

```
src/
├── main.tsx              # Entrada → app/App.tsx
├── app/                  # Shell, rutas, composición de features
├── features/             # dashboard, inbox, shipments, validation, notifications
├── components/ui/        # Primitivos (Button, Card, Modal…)
├── hooks/                # use-toast
├── lib/                  # axios, query-client, pdf-setup
├── stores/               # Zustand (rol, filtros, toasts)
├── types/                # Tipos de dominio compartidos
├── utils/                # formatters, state machine helpers
├── styles/               # tokens + Tailwind
└── testing/              # MSW + helpers de tests
```

**No debe existir** (scaffold viejo eliminado): `src/App.tsx`, `src/pages/`, `src/store/`, `src/api/`, `src/components/Layout.tsx`.

Carpetas vacías `features/*/api|hooks|types` sin archivos se pueden borrar; solo se mantienen las que tienen código (p. ej. `shipments/api`, `inbox/api`).

## Architecture (feature-based)

Dependency flow is **unidirectional**:

```
shared (components/ui, hooks, lib, utils, types, stores)
    ↑
features (dashboard, inbox, shipments, validation, notifications)
    ↑
app (routes, layout, providers — composes features)
```

### Rules (enforced by ESLint `import/no-restricted-paths`)

1. A **feature must not import another feature** directly.
2. **Shared layers** must not import from `features/` or `app/`.
3. **Cross-feature UI** is composed in `src/app/routes/` (e.g. `ShipmentDetailPage` wires shipments API + validation PDF view + approve modal).

Each feature exposes a public API via `index.ts`; consumers outside the feature import only from that barrel.

## Key screens

- **Dashboard** — status counts, pipeline overview, recent shipments
- **Inbox** — list PDFs, create shipment
- **Shipments** — filterable list with status badges
- **Shipment detail** — split PDF viewer + extracted / typed / comparison tabs; role-gated actions

## Design tokens

Brand colors live in `src/styles/tokens.css` (see `design-tokens.md`). Use Tailwind utilities (`bg-brand`, `text-accent`, etc.) — do not scatter raw hex in components.

## Testing

MSW handlers in `src/testing/handlers.ts` mock the backend. Tests cover status badges, diff highlighting, disabled validate actions, and the approve toast flow.
