# Naviera Docs — comandos desde PowerShell (funciona en rutas UNC del NAS)
# Uso: .\naviera.ps1 up   |   .\naviera.ps1 sync   |   .\naviera.ps1

param(
    [Parameter(Position = 0)]
    [string]$Command = 'help'
)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

function Show-Help {
    Write-Host ''
    Write-Host '  Naviera Docs — naviera.ps1' -ForegroundColor Cyan
    Write-Host "  Carpeta: $PSScriptRoot"
    Write-Host '  ============================'
    Write-Host ''
    Write-Host '  .\naviera.ps1 up          Levanta todo'
    Write-Host '  .\naviera.ps1 down        Baja todo'
    Write-Host '  .\naviera.ps1 restart     down + up'
    Write-Host '  .\naviera.ps1 rebuild     Rebuild + recrea'
    Write-Host '  .\naviera.ps1 sync        PDFs -> Docker'
    Write-Host '  .\naviera.ps1 status      docker compose ps'
    Write-Host '  .\naviera.ps1 check       Prueba API'
    Write-Host '  .\naviera.ps1 logs        Logs'
    Write-Host '  .\naviera.ps1 down-v      Borra volumenes'
    Write-Host ''
    Write-Host '  UI: http://localhost:5173   API: http://localhost:8000/docs'
    Write-Host ''
}

switch ($Command.ToLower()) {
    'help' { Show-Help }
    'up' { docker compose up -d --build }
    'down' { docker compose down }
    'down-v' { docker compose down -v }
    'restart' {
        docker compose down
        docker compose up -d --build
    }
    'rebuild' {
        docker compose build
        docker compose up -d --force-recreate
    }
    'build' { docker compose build }
    'sync' { & "$PSScriptRoot\scripts\sync-inbox.ps1" }
    'sync-inbox' { & "$PSScriptRoot\scripts\sync-inbox.ps1" }
    'status' { docker compose ps }
    'ps' { docker compose ps }
    'check' { & "$PSScriptRoot\scripts\check-api.bat" }
    'logs' { docker compose logs -f backend frontend }
    'install' { & "$PSScriptRoot\scripts\install-deps.ps1" }
    'test' { docker compose exec backend pytest tests -v }
    'migrate' { docker compose exec backend alembic upgrade head }
    'clean' { & "$PSScriptRoot\scripts\clean.ps1" }
    default {
        Write-Host "Comando desconocido: $Command" -ForegroundColor Red
        Show-Help
        exit 1
    }
}
