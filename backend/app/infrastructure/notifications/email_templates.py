"""HTML/plain bodies for client notification emails."""


def build_approval_email(
    *,
    client_name: str,
    reference: str,
    approval_url: str,
) -> tuple[str, str]:
    """Return (plain_text, html) for the notification email."""
    plain = (
        f"Estimado {client_name},\n\n"
        f"La documentación del embarque {reference} ha sido validada "
        "y está lista para su revisión.\n\n"
        f"Para aprobar la documentación, abra este enlace:\n{approval_url}\n\n"
        "Si no reconoce este envío, ignore este correo."
    )
    html = f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head>
<body style="font-family:system-ui,sans-serif;line-height:1.5;color:#1a1a2e;max-width:560px;margin:0 auto;padding:24px">
  <p>Estimado <strong>{_escape(client_name)}</strong>,</p>
  <p>La documentación del embarque <strong>{_escape(reference)}</strong> ha sido validada
     y está lista para su revisión. El PDF va adjunto a este correo.</p>
  <p style="margin:28px 0">
    <a href="{_escape(approval_url)}"
       style="display:inline-block;background:#5b4bb7;color:#fff;text-decoration:none;
              padding:14px 28px;border-radius:8px;font-weight:600;font-size:16px">
      Aprobar documentación
    </a>
  </p>
  <p style="font-size:13px;color:#666">Si el botón no funciona, copie este enlace en el navegador:<br>
    <a href="{_escape(approval_url)}">{_escape(approval_url)}</a></p>
  <p style="font-size:12px;color:#888">Si no reconoce este envío, ignore este correo.</p>
</body>
</html>"""
    return plain, html


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
