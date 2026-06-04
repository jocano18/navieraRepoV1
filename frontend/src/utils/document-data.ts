import type { BlFieldKey, Container, DigitizedPayload, DocumentData } from '@/types';
import { BL_FIELD_KEYS } from '@/types';

export function documentDataToFields(data: DocumentData): Record<string, string> {
  const fields: Record<string, string> = {};
  for (const key of BL_FIELD_KEYS) {
    fields[key] = data[key].value;
  }
  return fields;
}

export function emptyDigitizedPayload(): DigitizedPayload {
  const fields = Object.fromEntries(BL_FIELD_KEYS.map((k) => [k, ''])) as Record<
    BlFieldKey,
    string
  >;
  return {
    fields,
    freight_terms: null,
    containers: [],
    digitized_by: 'operator',
  };
}

export function digitizedFromDocument(data: DocumentData): DigitizedPayload {
  return {
    fields: documentDataToFields(data),
    freight_terms: data.freight_terms,
    containers: data.containers.map((c) => ({ ...c })),
    digitized_by: 'operator',
  };
}

export function emptyContainer(): Container {
  return {
    container_number: '',
    seal: '',
    container_type: '',
    packages: '',
    gross_weight_kgs: '',
    measurement_cbm: '',
  };
}
