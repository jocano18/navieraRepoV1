import { useEffect, useState } from 'react';

import { Badge, Button, Input, Modal } from '@/components/ui';
import type { CargoType, InboxPdf } from '@/types';
import {
  cargoTypeLabel,
  documentTypeLabel,
  inferDocumentType,
  suggestCargoType,
  type DocumentType,
} from '@/utils/document-type';

export function CreateShipmentModal({
  pdf,
  open,
  loading,
  onClose,
  onConfirm,
}: {
  pdf: InboxPdf | null;
  open: boolean;
  loading?: boolean;
  onClose: () => void;
  onConfirm: (payload: {
    filename: string;
    cargo_type: CargoType;
    reference: string;
  }) => void;
}) {
  const [cargoType, setCargoType] = useState<CargoType>('DIRECTO');
  const [reference, setReference] = useState('');
  const [docType, setDocType] = useState<DocumentType>('OTRO');

  useEffect(() => {
    if (!pdf) return;
    const detected = inferDocumentType(pdf.filename);
    setDocType(detected);
    setCargoType(suggestCargoType(pdf.filename, detected));
    setReference(pdf.filename.replace(/\.pdf$/i, ''));
  }, [pdf]);

  if (!pdf) return null;

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Crear envío desde PDF"
      description="Confirma el tipo de documento y carga antes de iniciar el flujo."
      size="lg"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancelar
          </Button>
          <Button
            loading={loading}
            onClick={() =>
              onConfirm({
                filename: pdf.filename,
                cargo_type: cargoType,
                reference: reference.trim() || pdf.filename,
              })
            }
          >
            Crear envío
          </Button>
        </>
      }
    >
      <div className="space-y-4">
        <div className="rounded-lg bg-lilac-soft px-4 py-3 text-sm">
          <p className="font-semibold text-brand">{pdf.filename}</p>
          <div className="mt-2 flex flex-wrap gap-2">
            <Badge tone="violet">{documentTypeLabel(docType)}</Badge>
            <Badge tone="cream">{cargoTypeLabel(cargoType)}</Badge>
          </div>
        </div>

        <div className="rounded-lg border border-border px-4 py-3 text-xs text-text-muted">
          <p>
            <strong className="text-brand">HBL</strong> (House): conocimiento de embarque de la
            carga del importador — suele ir en operaciones consolidadas.
          </p>
          <p className="mt-2">
            <strong className="text-brand">MBL</strong> (Master): conocimiento del naviero /
            consolidador — agrupa varios envíos.
          </p>
        </div>

        <fieldset className="space-y-2">
          <legend className="text-sm font-semibold text-brand">Tipo de carga (extracción)</legend>
          {(['DIRECTO', 'CONSOLIDADO'] as const).map((type) => (
            <label
              key={type}
              className="flex cursor-pointer items-start gap-3 rounded-lg border border-border px-3 py-2 has-[:checked]:border-accent has-[:checked]:bg-cream/50"
            >
              <input
                type="radio"
                name="cargo_type"
                value={type}
                checked={cargoType === type}
                className="mt-1"
                onChange={() => setCargoType(type)}
              />
              <span className="text-sm">
                <span className="font-semibold text-brand">{type}</span>
                <span className="block text-xs text-text-muted">{cargoTypeLabel(type)}</span>
              </span>
            </label>
          ))}
        </fieldset>

        <Input
          label="Referencia del envío"
          hint="Nombre interno para identificar el caso en listados y dashboard"
          value={reference}
          onChange={(e) => setReference(e.target.value)}
        />
      </div>
    </Modal>
  );
}
