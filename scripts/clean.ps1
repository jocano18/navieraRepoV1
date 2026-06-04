# Limpia cachés de pytest, mypy y __pycache__ del proyecto
$ErrorActionPreference = "SilentlyContinue"
$root = Split-Path -Parent $PSScriptRoot

Write-Host "Limpiando cachés en $root ..."

$patterns = @(
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "pytest-cache-files-*",
    ".coverage",
    "htmlcov",
    "*.egg-info"
)

foreach ($pattern in $patterns) {
    Get-ChildItem -Path $root -Recurse -Directory -Filter $pattern -ErrorAction SilentlyContinue |
        ForEach-Object {
            Write-Host "  Eliminando $($_.FullName)"
            Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
    Get-ChildItem -Path $root -Recurse -Directory -Filter "pytest-cache-files-*" -ErrorAction SilentlyContinue |
        ForEach-Object {
            Write-Host "  Eliminando $($_.FullName)"
            Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        }
}

Get-ChildItem -Path "$root\backend" -Directory -Filter "pytest-cache-files-*" -ErrorAction SilentlyContinue |
    ForEach-Object {
        cmd /c "rmdir /s /q `"$($_.FullName)`"" 2>$null
        Write-Host "  Eliminado (rmdir): $($_.Name)"
    }

Write-Host "Limpieza terminada."
