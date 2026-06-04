# B/L Inbox Folder

Drop Bill of Lading PDF files here. The system scans this folder via `GET /inbox/pdfs`.

## Sample carriers supported

- **AMASS** — uses dedicated `AmassExtractor` (grid LCL layout)
- **CMA CGM, Evergreen, ECU, YQN, DC Logistics, Schenker** — `GenericBlExtractor` (regex/labels)
- **Scanned PDFs** (e.g. Evergreen) — automatic Tesseract OCR fallback

## Testing

Copy 1–2 real B/L PDFs from your course materials into this folder, or into `tests/fixtures/`.

Default demo client ID (for API): `00000000-0000-0000-0000-000000000001`
