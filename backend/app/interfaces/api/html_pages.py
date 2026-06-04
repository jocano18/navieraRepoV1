"""Simple HTML pages for public email-approval flow."""


def approval_success_page(*, reference: str, status: str) -> str:
    """Thank-you page after client approves via email link."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Documentación aprobada</title>
</head>
<body style="font-family:system-ui,sans-serif;line-height:1.5;color:#1a1a2e;max-width:520px;margin:48px auto;padding:24px;text-align:center">
  <h1 style="color:#2d6a4f;font-size:1.5rem">Documentación aprobada</h1>
  <p>El embarque <strong>{_escape(reference)}</strong> fue aprobado correctamente.</p>
  <p style="color:#666;font-size:14px">Estado actual: <strong>{_escape(status)}</strong></p>
  <p style="color:#888;font-size:13px">Puede cerrar esta ventana.</p>
</body>
</html>"""


def approval_error_page(message: str) -> str:
    """Error page for invalid or expired approval links."""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>No se pudo aprobar</title>
</head>
<body style="font-family:system-ui,sans-serif;line-height:1.5;color:#1a1a2e;max-width:520px;margin:48px auto;padding:24px;text-align:center">
  <h1 style="color:#c1121f;font-size:1.5rem">No se pudo aprobar</h1>
  <p>{_escape(message)}</p>
  <p style="color:#888;font-size:13px">Contacte a su ejecutivo de cuenta si necesita un nuevo enlace.</p>
</body>
</html>"""


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
