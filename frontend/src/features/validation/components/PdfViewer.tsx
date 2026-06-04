import { useEffect, useState } from 'react';
import { ExternalLink } from 'lucide-react';

import { Button, Skeleton } from '@/components/ui';
import { fetchShipmentPdfBlob } from '@/lib/shipment-pdf';

/**
 * Visor PDF con iframe nativo del navegador (más fiable que pdf.js en Docker/Vite).
 */
export function PdfViewer({ shipmentId }: { shipmentId: string }) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);

  useEffect(() => {
    let objectUrl: string | undefined;
    setLoading(true);
    setLoadError(null);
    setPdfUrl(null);

    void fetchShipmentPdfBlob(shipmentId)
      .then((blob) => {
        objectUrl = URL.createObjectURL(blob);
        setPdfUrl(objectUrl);
      })
      .catch((err: { response?: { status?: number }; message?: string }) => {
        setLoadError(
          err.response?.status === 404
            ? 'PDF no encontrado en el almacén del envío.'
            : err.message ?? 'No se pudo cargar el PDF.',
        );
      })
      .finally(() => setLoading(false));

    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [shipmentId]);

  return (
    <div className="flex h-full min-h-[480px] flex-col rounded-card border border-border bg-surface">
      <div className="flex items-center justify-between gap-2 border-b border-border px-4 py-3">
        <span className="text-sm font-semibold text-brand">Documento original</span>
        {pdfUrl ? (
          <a href={pdfUrl} target="_blank" rel="noopener noreferrer">
            <Button variant="ghost" size="sm" type="button">
              <ExternalLink className="h-4 w-4" />
              Abrir en pestaña
            </Button>
          </a>
        ) : null}
      </div>
      <div className="flex flex-1 flex-col overflow-hidden bg-lilac-soft/40 p-2">
        {loading ? (
          <Skeleton className="min-h-[600px] w-full flex-1" />
        ) : loadError ? (
          <p className="p-4 text-sm text-coral" role="alert">
            {loadError}
          </p>
        ) : pdfUrl ? (
          <iframe
            src={pdfUrl}
            title="Documento PDF del envío"
            className="min-h-[600px] w-full flex-1 rounded-lg border border-border bg-white"
          />
        ) : null}
      </div>
    </div>
  );
}
