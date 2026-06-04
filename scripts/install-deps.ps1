# Instala dependencias locales de backend y frontend (sin Docker).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "=== Backend (Python) ===" -ForegroundColor Cyan
$Backend = Join-Path $Root "backend"
$Venv = Join-Path $Backend ".venv"
if (-not (Test-Path $Venv)) {
    python -m venv $Venv
}
& (Join-Path $Venv "Scripts" "pip.exe") install -r (Join-Path $Backend "requirements.txt")

Write-Host "=== Frontend (npm) ===" -ForegroundColor Cyan
$Frontend = Join-Path $Root "frontend"
Push-Location $Frontend
npm install
Pop-Location

Write-Host "Listo. Levanta con: docker compose up --build" -ForegroundColor Green
