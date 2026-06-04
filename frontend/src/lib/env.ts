export function getApiBaseUrl(): string {
  // Dev: mismo origen (5173) → proxy de Vite reenvía al backend (evita CORS y hosts incorrectos).
  if (import.meta.env.DEV) {
    return '';
  }
  const url = import.meta.env.VITE_API_URL ?? import.meta.env.VITE_API_BASE_URL;
  if (!url || typeof url !== 'string') {
    return 'http://localhost:8000';
  }
  return url.replace(/\/$/, '');
}
