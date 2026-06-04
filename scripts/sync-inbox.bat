@echo off
setlocal EnableExtensions
REM pushd mapea rutas UNC (NAS) a una letra de unidad temporal; cd /d falla en \\servidor\...
pushd "%~dp0\.." || (
    echo.
    echo ERROR: No se puede acceder al proyecto en red UNC.
    echo Mapea el NAS a una unidad, por ejemplo:
    echo   net use Z: "\\nas2021.newcreangel.local\share1"
    echo   Z:
    echo   cd "Z:\jocano\My Documents\My Videos\navieraV2"
    echo   scripts\sync-inbox.bat
    exit /b 1
)

echo Copiando PDFs desde:
echo   %CD%\backend\data\inbox
echo hacia naviera-backend:/app/data/inbox ...
echo.

docker cp "backend\data\inbox\." naviera-backend:/app/data/inbox/
set "ERR=%ERRORLEVEL%"

popd

if not "%ERR%"=="0" (
    echo.
    echo ERROR: docker cp fallo. Comprueba que el backend este en marcha:
    echo   docker compose ps
    echo   docker compose up -d
    exit /b 1
)

echo.
echo Listo. Prueba: curl.exe http://localhost:8000/inbox/pdfs
endlocal
