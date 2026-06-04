export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat('es-CO', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(iso));
}

export function formatFieldLabel(key: string): string {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function inferCarrierFromFilename(filename: string): string | null {
  const lower = filename.toLowerCase();
  if (lower.includes('maersk')) return 'Maersk';
  if (lower.includes('msc')) return 'MSC';
  if (lower.includes('cosco')) return 'COSCO';
  if (lower.includes('hapag')) return 'Hapag-Lloyd';
  return null;
}
