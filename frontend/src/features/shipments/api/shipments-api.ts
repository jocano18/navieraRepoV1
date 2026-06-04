import { apiClient } from '@/lib/api-client';
import type {
  ComparisonResponse,
  DigitizedPayload,
  DocumentData,
  ShipmentDetail,
  ShipmentStatus,
  ShipmentSummary,
  ValidateResponse,
} from '@/types';

export async function fetchShipments(params?: {
  status?: ShipmentStatus;
  skip?: number;
  limit?: number;
}): Promise<ShipmentSummary[]> {
  const { data } = await apiClient.get<ShipmentSummary[]>('/shipments', { params });
  return data;
}

export async function fetchShipment(id: string): Promise<ShipmentDetail> {
  const { data } = await apiClient.get<ShipmentDetail>(`/shipments/${id}`);
  return data;
}

export async function createShipment(body: {
  source_pdf_filename: string;
  cargo_type: string;
  client_id: string;
  reference?: string;
}): Promise<ShipmentSummary> {
  const { data } = await apiClient.post<ShipmentSummary>('/shipments', body);
  return data;
}

export async function extractShipment(id: string): Promise<DocumentData> {
  const { data } = await apiClient.post<{ data: DocumentData }>(
    `/shipments/${id}/extract`,
  );
  return data.data;
}

export async function registerDigitized(
  id: string,
  payload: DigitizedPayload,
): Promise<void> {
  await apiClient.post(`/shipments/${id}/digitized-data`, payload);
}

export async function correctDigitized(
  id: string,
  payload: DigitizedPayload,
): Promise<void> {
  await apiClient.patch(`/shipments/${id}/digitized-data`, payload);
}

export async function fetchComparison(id: string): Promise<ComparisonResponse> {
  const { data } = await apiClient.get<ComparisonResponse>(
    `/shipments/${id}/comparison`,
  );
  return data;
}

export async function validateShipment(
  id: string,
  markComplete: boolean,
): Promise<ValidateResponse> {
  const { data } = await apiClient.post<ValidateResponse>(
    `/shipments/${id}/validate`,
    { mark_complete: markComplete },
  );
  return data;
}

export async function approveShipment(id: string): Promise<void> {
  await apiClient.post(`/shipments/${id}/approve`);
}

export async function registerNovelty(id: string, description: string): Promise<void> {
  await apiClient.post(`/shipments/${id}/novelty`, { description });
}
