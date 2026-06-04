import { http, HttpResponse } from 'msw';

import type {
  ComparisonResponse,
  DocumentData,
  ShipmentDetail,
  ShipmentSummary,
} from '@/types';
import { DEFAULT_CLIENT_ID } from '@/types';

const API = 'http://localhost:8000';

const mockExtracted: DocumentData = {
  bl_number: { value: 'BL-2024-001', source: 'NATIVE' },
  carrier_name: { value: 'Maersk Line', source: 'NATIVE' },
  shipper: { value: 'ACME Corp', source: 'OCR' },
  consignee: { value: 'Importadora SA', source: 'NATIVE' },
  notify_party: { value: '', source: 'NOT_FOUND' },
  delivery_agent: { value: 'Agent Co', source: 'NATIVE' },
  vessel_and_voyage: { value: 'MV NAVIERA / 042E', source: 'NATIVE' },
  place_of_receipt: { value: 'Bogotá', source: 'NATIVE' },
  port_of_loading: { value: 'Cartagena', source: 'NATIVE' },
  port_of_discharge: { value: 'Miami', source: 'NATIVE' },
  place_of_delivery: { value: 'Miami, FL', source: 'NATIVE' },
  marks_and_numbers: { value: 'N/M', source: 'NATIVE' },
  description_of_goods: { value: 'General cargo', source: 'NATIVE' },
  number_of_packages: { value: '100', source: 'NATIVE' },
  gross_weight_kgs: { value: '12500', source: 'NATIVE' },
  measurement_cbm: { value: '42', source: 'NATIVE' },
  number_of_originals: { value: '3', source: 'NATIVE' },
  shipped_on_board_date: { value: '2024-06-01', source: 'NATIVE' },
  freight_terms: 'PREPAID',
  containers: [],
  text_source: 'NATIVE',
};

let shipments: ShipmentDetail[] = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    reference: 'REF-001',
    status: 'EN_VALIDACION',
    cargo_type: 'DIRECTO',
    source_pdf_filename: 'test.pdf',
    client_id: DEFAULT_CLIENT_ID,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    novelty_description: '',
    extracted_data: null,
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    reference: 'REF-002',
    status: 'COMPLETO',
    cargo_type: 'DIRECTO',
    source_pdf_filename: 'sample.pdf',
    client_id: DEFAULT_CLIENT_ID,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    novelty_description: '',
    extracted_data: null,
  },
];

function comparisonFor(shipmentId: string, mismatch = true): ComparisonResponse {
  return {
    shipment_id: shipmentId,
    is_complete: !mismatch,
    fields: [
      {
        field: 'bl_number',
        extracted_value: 'BL-2024-001',
        typed_value: mismatch ? 'BL-WRONG' : 'BL-2024-001',
        matches: !mismatch,
        source: 'NATIVE',
      },
      {
        field: 'shipper',
        extracted_value: 'ACME Corp',
        typed_value: 'ACME Corp',
        matches: true,
        source: 'OCR',
      },
    ],
  };
}

export const handlers = [
  http.get(`${API}/inbox/pdfs`, () =>
    HttpResponse.json([{ filename: 'test.pdf', size_bytes: 2048 }]),
  ),
  http.get(`${API}/shipments`, ({ request }) => {
    const url = new URL(request.url);
    const status = url.searchParams.get('status');
    let list: ShipmentSummary[] = shipments;
    if (status) {
      list = list.filter((s) => s.status === status);
    }
    return HttpResponse.json(list);
  }),
  http.get(`${API}/shipments/:id`, ({ params }) => {
    const s = shipments.find((x) => x.id === params.id);
    if (!s) return HttpResponse.json({ detail: 'Not found' }, { status: 404 });
    return HttpResponse.json(s);
  }),
  http.get(`${API}/shipments/:id/comparison`, ({ params }) => {
    const mismatch = params.id === '11111111-1111-1111-1111-111111111111';
    return HttpResponse.json(comparisonFor(String(params.id), mismatch));
  }),
  http.post(`${API}/shipments/:id/validate`, async ({ params, request }) => {
    const body = (await request.json()) as { mark_complete: boolean };
    const s = shipments.find((x) => x.id === params.id);
    if (!s) return HttpResponse.json({}, { status: 404 });
    s.status = body.mark_complete ? 'COMPLETO' : 'INCOMPLETO';
    s.updated_at = new Date().toISOString();
    return HttpResponse.json({ shipment_id: s.id, new_status: s.status });
  }),
  http.post(`${API}/shipments/:id/approve`, ({ params }) => {
    const s = shipments.find((x) => x.id === params.id);
    if (!s) return HttpResponse.json({}, { status: 404 });
    s.status = 'NOTIFICADO';
    return new HttpResponse(null, { status: 204 });
  }),
  http.post(`${API}/shipments/:id/extract`, () =>
    HttpResponse.json({ data: mockExtracted }),
  ),
];
