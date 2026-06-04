import { apiClient } from './api-client';

async function assertPdfBlob(blob: Blob): Promise<Blob> {
  if (!(blob instanceof Blob) || blob.size === 0) {
    throw new Error('El servidor devolvió un PDF vacío.');
  }
  const header = await blob.slice(0, 5).text();
  if (!header.startsWith('%PDF')) {
    throw new Error(
      'El servidor no devolvió un PDF válido. ¿Está el backend en marcha?',
    );
  }
  return blob;
}

export async function fetchShipmentPdfBlob(shipmentId: string): Promise<Blob> {
  try {
    const { data } = await apiClient.get<Blob>(`/shipments/${shipmentId}/pdf`, {
      responseType: 'blob',
    });
    return await assertPdfBlob(data);
  } catch (error) {
    if (error instanceof Error && error.message.includes('PDF')) {
      throw error;
    }
    throw error;
  }
}
