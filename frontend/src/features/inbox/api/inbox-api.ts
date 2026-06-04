import { apiClient } from '@/lib/api-client';
import type { InboxPdf, ShipmentSummary } from '@/types';

export async function fetchInboxPdfs(): Promise<InboxPdf[]> {
  const { data } = await apiClient.get<InboxPdf[]>('/inbox/pdfs');
  return data;
}

export async function createShipmentFromInbox(body: {
  source_pdf_filename: string;
  cargo_type: string;
  client_id: string;
  reference?: string;
}): Promise<ShipmentSummary> {
  const { data } = await apiClient.post<ShipmentSummary>('/shipments', body);
  return data;
}
