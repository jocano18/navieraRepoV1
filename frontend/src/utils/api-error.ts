import axios from 'axios';

export function getApiErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === 'string' && detail.length > 0) {
      return detail;
    }
    if (Array.isArray(detail)) {
      return detail
        .map((item) => {
          if (typeof item === 'object' && item !== null && 'msg' in item) {
            return String((item as { msg: string }).msg);
          }
          return JSON.stringify(item);
        })
        .join('; ');
    }
    if (error.response?.status === 404) {
      return 'Recurso no encontrado en el servidor.';
    }
    if (!error.response) {
      const hint = import.meta.env.DEV
        ? 'Comprueba que los contenedores estén arriba: docker compose ps y docker compose logs backend --tail 40'
        : '¿Está el backend en http://localhost:8000?';
      const code = error.code ? ` (${error.code})` : '';
      return `No hay conexión con el API${code}. ${hint}`;
    }
  }
  if (error instanceof Error && error.message) {
    return error.message;
  }
  return fallback;
}
