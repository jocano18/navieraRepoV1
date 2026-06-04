# Quita del indice de Git archivos de cache ya rastreados (.gitignore no aplica a lo ya indexado).
$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

$cachePattern = '(\\|/)?(__pycache__|\.pytest_cache|pytest-cache-files|\.mypy_cache|\.ruff_cache|\.pytype|node_modules|\.vite|htmlcov|\.coverage|\.cache)(\\|/|$)'

Write-Host 'Buscando caches en el indice de Git...' -ForegroundColor Cyan
$paths = git ls-files -c | Where-Object { $_ -match $cachePattern }

if (-not $paths) {
    Write-Host 'No hay archivos de cache en el indice. Solo asegurate de no hacer git add de esas carpetas.' -ForegroundColor Green
    exit 0
}

foreach ($path in $paths) {
    Write-Host "  git rm --cached $path"
    git rm -r --cached --ignore-unmatch $path 2>$null
}

Write-Host "Listo ($($paths.Count) rutas). Ejecuta: git status" -ForegroundColor Green
