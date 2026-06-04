import type { CargoType } from '@/types';

export type DocumentType = 'HBL' | 'MBL' | 'OTRO';

const DOC_LABELS: Record<DocumentType, string> = {
  HBL: 'HBL — House Bill of Lading',
  MBL: 'MBL — Master Bill of Lading',
  OTRO: 'Documento B/L',
};

const CARGO_LABELS: Record<CargoType, string> = {
  DIRECTO: 'Carga directa (un consignatario principal)',
  CONSOLIDADO: 'Carga consolidada (varios HBL bajo un MBL)',
};

/** Detecta tipo de documento por el nombre del archivo. */
export function inferDocumentType(filename: string): DocumentType {
  const upper = filename.toUpperCase();
  if (upper.includes('MBL')) return 'MBL';
  if (upper.includes('HBL')) return 'HBL';
  return 'OTRO';
}

/** Sugiere tipo de carga según nombre y tipo de documento. */
export function suggestCargoType(filename: string, docType: DocumentType): CargoType {
  if (filename.toLowerCase().includes('directo')) return 'DIRECTO';
  if (docType === 'MBL') return 'CONSOLIDADO';
  if (docType === 'HBL') return 'CONSOLIDADO';
  return 'DIRECTO';
}

export function documentTypeLabel(docType: DocumentType): string {
  return DOC_LABELS[docType];
}

export function cargoTypeLabel(cargo: CargoType): string {
  return CARGO_LABELS[cargo];
}
