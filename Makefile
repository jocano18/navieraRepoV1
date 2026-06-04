# Naviera Docs — comandos de despliegue local (Docker)
# Windows sin GNU Make: usa  make.bat up   o   .\make.bat sync

.PHONY: help up up-fg down down-v restart rebuild build logs ps status sync sync-inbox check install test migrate clean shell-backend shell-frontend

COMPOSE := docker compose
BACKEND := $(COMPOSE) exec backend

# Windows: sync vía .bat (pushd para rutas UNC del NAS)
ifeq ($(OS),Windows_NT)
  SYNC_INBOX := cmd /c scripts\sync-inbox.bat
  CHECK_API := cmd /c scripts\check-api.bat
else
  SYNC_INBOX := powershell -ExecutionPolicy Bypass -File scripts/sync-inbox.ps1
  CHECK_API := curl -sf http://localhost:8000/health && curl -sf http://localhost:8000/inbox/pdfs | head -c 200
endif

.DEFAULT_GOAL := help

help: ## Lista de comandos
	@echo.
	@echo   Naviera Docs — despliegue con Docker
	@echo   =====================================
	@echo.
	@echo   make up          Levanta todo (build + segundo plano)
	@echo   make down        Para y quita contenedores
	@echo   make restart     down + up
	@echo   make rebuild     Reconstruye imagenes y recrea contenedores
	@echo   make sync        Copia PDFs de backend/data/inbox al contenedor
	@echo   make status      Estado de los contenedores
	@echo   make check       Prueba health + inbox + crear envio
	@echo   make logs        Logs de backend y frontend
	@echo   make build       Solo construye imagenes
	@echo   make install     Dependencias locales (venv + npm, opcional)
	@echo   make test        pytest en el contenedor backend
	@echo   make migrate     Alembic upgrade head
	@echo   make clean       Limpia caches Python
	@echo   make down-v      down + borra volumenes (reset BD/inbox)
	@echo.
	@echo   URLs:  http://localhost:5173   http://localhost:8000/docs
	@echo.

up: ## Levanta todos los servicios
	$(COMPOSE) up -d --build

up-fg: ## Levanta en primer plano (ver logs en la misma ventana)
	$(COMPOSE) up --build

down: ## Baja todos los servicios
	$(COMPOSE) down

down-v: ## Baja servicios y elimina volumenes (reset completo)
	$(COMPOSE) down -v

restart: down up ## Reinicia todo

rebuild: ## Reconstruye imagenes y recrea contenedores
	$(COMPOSE) build
	$(COMPOSE) up -d --force-recreate

build: ## Construye imagenes sin arrancar
	$(COMPOSE) build

logs: ## Sigue logs de backend y frontend
	$(COMPOSE) logs -f backend frontend

ps status: ## Estado de contenedores
	$(COMPOSE) ps

sync: sync-inbox ## Sincroniza PDFs del host al volumen Docker

sync-inbox: ## Copia backend/data/inbox -> naviera-backend:/app/data/inbox
	$(SYNC_INBOX)

check: ## Comprueba que el API responde
	$(CHECK_API)

install: ## Instala deps locales (IDE); el dia a dia es solo Docker
	powershell -ExecutionPolicy Bypass -File scripts/install-deps.ps1

test: ## Tests backend en contenedor
	$(BACKEND) pytest tests -v

migrate: ## Migraciones Alembic
	$(BACKEND) alembic upgrade head

clean: ## Limpia caches pytest/mypy
	powershell -ExecutionPolicy Bypass -File scripts/clean.ps1

shell-backend: ## Shell en contenedor backend
	$(COMPOSE) exec backend bash

shell-frontend: ## Shell en contenedor frontend
	$(COMPOSE) exec frontend sh
