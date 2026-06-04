@echo off
setlocal
echo === Health ===
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:8000/health
if errorlevel 1 (
    echo.
    echo El backend no responde. Espera 20s y revisa: docker compose logs backend --tail 30
    exit /b 1
)
echo.
echo === Inbox PDFs ===
curl.exe -s -w "\nHTTP %%{http_code}\n" http://localhost:8000/inbox/pdfs
echo.
echo === Crear envio (POST /shipments) ===
curl.exe -s -w "\nHTTP %%{http_code}\n" -X POST http://localhost:8000/shipments ^
  -H "Content-Type: application/json" ^
  -d "{\"source_pdf_filename\":\"311SSA50720.pdf\",\"cargo_type\":\"DIRECTO\",\"client_id\":\"00000000-0000-0000-0000-000000000001\",\"reference\":\"test-api-check\"}"
echo.
echo Si POST devuelve 404/422 pero no conexion, el API responde. Si falla conexion, revisa: docker compose logs backend --tail 40
endlocal
