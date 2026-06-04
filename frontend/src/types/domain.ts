export type CargoType = 'DIRECTO' | 'CONSOLIDADO';

export type ShipmentStatus =
  | 'PENDIENTE_EXTRACCION'
  | 'EXTRAIDO'
  | 'EN_DIGITACION'
  | 'EN_VALIDACION'
  | 'INCOMPLETO'
  | 'COMPLETO'
  | 'NOTIFICADO'
  | 'APROBADO_CLIENTE'
  | 'CON_NOVEDAD'
  | 'FINALIZADO'
  | 'RECHAZADO';

export type FieldSource = 'NATIVE' | 'OCR' | 'NOT_FOUND';

export type UserRole = 'operator' | 'executive';

export interface ExtractedField {
  value: string;
  source: FieldSource;
}

export interface Container {
  container_number: string;
  seal: string;
  container_type: string;
  packages: string;
  gross_weight_kgs: string;
  measurement_cbm: string;
}

export interface DocumentData {
  bl_number: ExtractedField;
  carrier_name: ExtractedField;
  shipper: ExtractedField;
  consignee: ExtractedField;
  notify_party: ExtractedField;
  delivery_agent: ExtractedField;
  vessel_and_voyage: ExtractedField;
  place_of_receipt: ExtractedField;
  port_of_loading: ExtractedField;
  port_of_discharge: ExtractedField;
  place_of_delivery: ExtractedField;
  marks_and_numbers: ExtractedField;
  description_of_goods: ExtractedField;
  number_of_packages: ExtractedField;
  gross_weight_kgs: ExtractedField;
  measurement_cbm: ExtractedField;
  number_of_originals: ExtractedField;
  shipped_on_board_date: ExtractedField;
  freight_terms: string | null;
  containers: Container[];
  text_source: FieldSource;
}

export interface ShipmentSummary {
  id: string;
  reference: string;
  status: ShipmentStatus;
  cargo_type: CargoType;
  source_pdf_filename: string;
  client_id: string;
  created_at: string;
}

export interface ShipmentDetail extends ShipmentSummary {
  novelty_description: string;
  updated_at: string;
  extracted_data: DocumentData | null;
}

export interface InboxPdf {
  filename: string;
  size_bytes: number;
}

export interface FieldComparison {
  field: string;
  extracted_value: string;
  typed_value: string;
  matches: boolean;
  source: FieldSource;
}

export interface ComparisonResponse {
  shipment_id: string;
  is_complete: boolean;
  fields: FieldComparison[];
}

export interface DigitizedPayload {
  fields: Record<string, string>;
  freight_terms: string | null;
  containers: Container[];
  digitized_by: string;
}

export interface ValidateResponse {
  shipment_id: string;
  new_status: ShipmentStatus;
}

export const BL_FIELD_KEYS = [
  'bl_number',
  'carrier_name',
  'shipper',
  'consignee',
  'notify_party',
  'delivery_agent',
  'vessel_and_voyage',
  'place_of_receipt',
  'port_of_loading',
  'port_of_discharge',
  'place_of_delivery',
  'marks_and_numbers',
  'description_of_goods',
  'number_of_packages',
  'gross_weight_kgs',
  'measurement_cbm',
  'number_of_originals',
  'shipped_on_board_date',
] as const;

export type BlFieldKey = (typeof BL_FIELD_KEYS)[number];

export const DEFAULT_CLIENT_ID = '00000000-0000-0000-0000-000000000001';

export const DEMO_CLIENT = {
  id: DEFAULT_CLIENT_ID,
  name: 'Demo Import Client',
  nit: '900123456-1',
  email: 'client@naviera.local',
};
