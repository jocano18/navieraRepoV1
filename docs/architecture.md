# Architecture — Naviera Documentation Management System

## Overview

The system follows **Clean Architecture** (Uncle Bob) organized as a monorepo with a Python/FastAPI backend and a React/TypeScript frontend. Dependencies point **inward**: outer layers depend on inner abstractions, never the reverse.

```
┌─────────────────────────────────────────────────────────────┐
│  interfaces/api   (FastAPI routers, schemas, DI)            │
├─────────────────────────────────────────────────────────────┤
│  infrastructure   (SQLAlchemy, PDF, email, storage, config) │
├─────────────────────────────────────────────────────────────┤
│  application      (use cases, ports, DTOs)                  │
├─────────────────────────────────────────────────────────────┤
│  domain           (entities, value objects, state machine)  │
└─────────────────────────────────────────────────────────────┘
```

## Layer responsibilities

### Domain (`backend/app/domain/`)

Pure business model. **No external libraries** except the Python standard library.

| Module | Contents |
|--------|----------|
| `entities/` | `Shipment` (aggregate root), `MBL`, `DocumentData`, `DigitizedData`, `ValidationResult`, `Client`, `Notification` |
| `value_objects/` | `CargoType`, `ShipmentStatus` |
| `state_machine/` | State pattern for shipment lifecycle transitions |
| `exceptions/` | `DomainError`, `InvalidStateTransitionError`, etc. |

### Application (`backend/app/application/`)

Orchestrates domain rules via **use cases**. Defines **ports** (abstract interfaces) that infrastructure must implement.

| Module | Contents |
|--------|----------|
| `ports/` | `PdfExtractor`, `ShipmentRepository`, `Notifier`, `FileStorage` |
| `use_cases/` | `ExtractPdfData`, `RegisterDigitizedData`, `CompareData`, … |
| `dto/` | Input/output structures crossing use case boundaries |

### Infrastructure (`backend/app/infrastructure/`)

Adapters for databases, PDF parsing, email, and filesystem storage.

| Module | Contents |
|--------|----------|
| `persistence/` | SQLAlchemy engine, `SqlAlchemyShipmentRepository` |
| `pdf/` | Strategy + Factory for direct vs consolidated cargo extraction |
| `notifications/` | `EmailNotifier` + Observer `NotificationSubject` |
| `storage/` | `LocalFileStorage` |
| `config/` | Pydantic `Settings` from environment |

### Interfaces (`backend/app/interfaces/api/`)

HTTP delivery mechanism: FastAPI routers, Pydantic request/response schemas, and FastAPI `Depends()` wiring.

## Design patterns (justification)

| Pattern | Location | Why |
|---------|----------|-----|
| **Repository** | `ShipmentRepository` port → `SqlAlchemyShipmentRepository` | Decouples domain from ORM; enables testing with in-memory fakes |
| **Strategy** | `DirectCargoExtractor`, `ConsolidatedCargoExtractor` | Different PDF layouts require different extraction algorithms without `if/else` in use cases |
| **Factory** | `PdfExtractorFactory` | Selects the correct strategy from `CargoType` in one place (Open/Closed) |
| **State** | `ShipmentState` / `ShipmentStateMachine` | Encapsulates valid transitions per status; avoids scattered transition logic |
| **Observer** | `NotificationObserver`, `NotificationSubject` | Allows audit logs, webhooks, or metrics on notification events without modifying `EmailNotifier` |
| **Dependency Injection** | `interfaces/api/dependencies.py` | Wires concrete adapters to use cases at the framework boundary |

## SOLID mapping

- **S** — Each use case class handles one application action.
- **O** — New cargo types add a new `PdfExtractor` strategy + factory registration without changing existing extractors.
- **L** — All repository/extractor implementations honor their port contracts.
- **I** — Small, focused ports (`Notifier`, `FileStorage`) instead of a god interface.
- **D** — Use cases depend on `ShipmentRepository` abstraction, not SQLAlchemy.

## Frontend structure

```
frontend/src/
  api/         HTTP client (calls backend /health, future REST)
  components/  Reusable UI (Layout)
  pages/       Route-level views (HomePage)
  store/       Client state placeholder
  types/       TypeScript mirrors of domain enums/DTOs
```

## Phase 1 scope

This document describes the **scaffold**. Business logic, ORM models, migrations, and REST endpoints beyond `/health` are deferred to Phase 2.
