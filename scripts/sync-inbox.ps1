# Copia PDFs de backend/data/inbox al volumen Docker (Windows + NAS/UNC).
# Si PowerShell bloquea el script, usa: scripts\sync-inbox.bat
$ErrorActionPreference = 'Stop'

$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Inbox = Join-Path $Root 'backend\data\inbox'

if (-not (Test-Path $Inbox)) {
    Write-Error "No existe la carpeta: $Inbox"
}

$running = docker ps --filter 'name=naviera-backend' --filter 'status=running' -q
if (-not $running) {
    Write-Host 'El contenedor naviera-backend no esta en ejecucion. Levanta primero:' -ForegroundColor Yellow
    Write-Host '  docker compose up -d' -ForegroundColor Yellow
    exit 1
}

Write-Host "Copiando PDFs desde $Inbox ..." -ForegroundColor Cyan
# Ruta absoluta evita problemas con el directorio actual en UNC
docker cp "${Inbox}${([IO.Path]::DirectorySeparatorChar)}." naviera-backend:/app/data/inbox/

$count = (Get-ChildItem $Inbox -Filter '*.pdf').Count
Write-Host "Listo. $count PDF(s) en el host." -ForegroundColor Green
Write-Host 'Verifica: curl.exe http://localhost:8000/inbox/pdfs' -ForegroundColor Green
