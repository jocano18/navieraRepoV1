@echo off
setlocal EnableExtensions

REM CMD no admite UNC como directorio actual; pushd asigna letra de unidad temporal.
pushd "%~dp0" || (
    echo.
    echo ERROR: No se puede acceder al proyecto en red UNC desde CMD.
    echo.
    echo Opcion A - Usa PowerShell en esta carpeta:
    echo   .\naviera.ps1 up
    echo.
    echo Opcion B - Mapea el NAS a una unidad:
    echo   net use Z: "\\nas2021.newcreangel.local\share1"
    echo   cd /d "Z:\jocano\My Documents\My Videos\navieraV2"
    echo   make.bat up
    echo.
    exit /b 1
)

set "CMD=%~1"
if "%CMD%"=="" set "CMD=help"
set "ERR=0"

if /i "%CMD%"=="help" goto help
if /i "%CMD%"=="up" goto up
if /i "%CMD%"=="down" goto down
if /i "%CMD%"=="down-v" goto downv
if /i "%CMD%"=="restart" goto restart
if /i "%CMD%"=="rebuild" goto rebuild
if /i "%CMD%"=="build" goto build
if /i "%CMD%"=="sync" goto sync
if /i "%CMD%"=="sync-inbox" goto sync
if /i "%CMD%"=="status" goto status
if /i "%CMD%"=="ps" goto status
if /i "%CMD%"=="check" goto check
if /i "%CMD%"=="logs" goto logs
if /i "%CMD%"=="install" goto install
if /i "%CMD%"=="test" goto test
if /i "%CMD%"=="migrate" goto migrate
if /i "%CMD%"=="clean" goto clean

echo Comando desconocido: %CMD%
set ERR=1
goto done

:help
echo.
echo   Naviera Docs — make.bat
echo   Carpeta activa: %CD%
echo   =========================
echo.
echo   make.bat up          Levanta todo
echo   make.bat down        Baja todo
echo   make.bat restart     down + up
echo   make.bat rebuild     Rebuild + recrea contenedores
echo   make.bat sync        PDFs host -^> Docker
echo   make.bat status      docker compose ps
echo   make.bat check       Prueba API
echo   make.bat logs        Logs backend + frontend
echo   make.bat down-v      down + borra volumenes
echo.
echo   En PowerShell tambien: .\naviera.ps1 up
echo   UI: http://localhost:5173   API: http://localhost:8000/docs
echo.
goto done

:up
docker compose up -d --build
set ERR=%ERRORLEVEL%
goto done

:down
docker compose down
set ERR=%ERRORLEVEL%
goto done

:downv
docker compose down -v
set ERR=%ERRORLEVEL%
goto done

:restart
docker compose down
if errorlevel 1 set ERR=1 & goto done
docker compose up -d --build
set ERR=%ERRORLEVEL%
goto done

:rebuild
docker compose build
if errorlevel 1 set ERR=1 & goto done
docker compose up -d --force-recreate
set ERR=%ERRORLEVEL%
goto done

:build
docker compose build
set ERR=%ERRORLEVEL%
goto done

:sync
call "%~dp0scripts\sync-inbox.bat"
set ERR=%ERRORLEVEL%
goto done

:status
docker compose ps
set ERR=%ERRORLEVEL%
goto done

:check
call "%~dp0scripts\check-api.bat"
set ERR=%ERRORLEVEL%
goto done

:logs
docker compose logs -f backend frontend
set ERR=%ERRORLEVEL%
goto done

:install
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\install-deps.ps1"
set ERR=%ERRORLEVEL%
goto done

:test
docker compose exec backend pytest tests -v
set ERR=%ERRORLEVEL%
goto done

:migrate
docker compose exec backend alembic upgrade head
set ERR=%ERRORLEVEL%
goto done

:clean
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\clean.ps1"
set ERR=%ERRORLEVEL%
goto done

:done
popd
exit /b %ERR%
