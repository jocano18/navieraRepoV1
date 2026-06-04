import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Inbox, Plus } from 'lucide-react';
import { motion } from 'framer-motion';

import { Badge, Button, Card, CardBody, EmptyState, Skeleton } from '@/components/ui';
import { useToast } from '@/hooks/use-toast';
import { DEFAULT_CLIENT_ID } from '@/types';
import type { CargoType, InboxPdf } from '@/types';
import { getApiErrorMessage } from '@/utils/api-error';
import { formatBytes, inferCarrierFromFilename } from '@/utils/format';
import {
  documentTypeLabel,
  inferDocumentType,
  type DocumentType,
} from '@/utils/document-type';
import { useCreateShipmentFromInbox, useInboxPdfs } from '../api/use-inbox';
import { CreateShipmentModal } from './CreateShipmentModal';
import { WorkflowGuide } from './WorkflowGuide';

const DOC_BADGE_TONE: Record<DocumentType, 'violet' | 'accent' | 'muted'> = {
  HBL: 'violet',
  MBL: 'accent',
  OTRO: 'muted',
};

export function InboxPage() {
  const { data, isLoading, isError } = useInboxPdfs();
  const createMutation = useCreateShipmentFromInbox();
  const navigate = useNavigate();
  const toast = useToast();
  const [selectedPdf, setSelectedPdf] = useState<InboxPdf | null>(null);
  const [modalOpen, setModalOpen] = useState(false);

  const handleConfirmCreate = async (payload: {
    filename: string;
    cargo_type: CargoType;
    reference: string;
  }) => {
    try {
      const shipment = await createMutation.mutateAsync({
        source_pdf_filename: payload.filename,
        cargo_type: payload.cargo_type,
        client_id: DEFAULT_CLIENT_ID,
        reference: payload.reference,
      });
      setModalOpen(false);
      setSelectedPdf(null);
      toast.success('Envío creado', `Referencia ${shipment.reference}`);
      void navigate(`/shipments/${shipment.id}`);
    } catch (error) {
      toast.error('No se pudo crear el envío', getApiErrorMessage(error, 'Error desconocido'));
    }
  };

  const openCreateModal = (pdf: InboxPdf) => {
    setSelectedPdf(pdf);
    setModalOpen(true);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-brand">Bandeja de entrada</h1>
        <p className="mt-1 text-text-muted">
          PDFs listos para convertirse en expedientes. Revisa HBL/MBL antes de crear el envío.
        </p>
      </div>

      <WorkflowGuide />

      {isError ? (
        <p className="text-sm text-coral" role="alert">
          No se pudo cargar la bandeja de entrada.
        </p>
      ) : isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
      ) : !data?.length ? (
        <EmptyState
          icon={Inbox}
          title="Bandeja vacía"
          description="Coloca archivos PDF en backend/data/inbox y ejecuta scripts\sync-inbox.bat"
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {data.map((pdf, index) => {
            const carrier = inferCarrierFromFilename(pdf.filename);
            const docType = inferDocumentType(pdf.filename);
            return (
              <motion.div
                key={pdf.filename}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.04 }}
              >
                <Card className="flex h-full flex-col transition-shadow hover:shadow-elevated">
                  <CardBody className="flex flex-1 flex-col">
                    <div className="mb-2 flex flex-wrap gap-2">
                      <Badge tone={DOC_BADGE_TONE[docType]}>
                        {docType === 'OTRO' ? 'B/L' : docType}
                      </Badge>
                      {carrier ? <Badge tone="muted">{carrier}</Badge> : null}
                    </div>
                    <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-brand text-accent">
                      <FileText className="h-5 w-5" aria-hidden />
                    </div>
                    <h3 className="truncate font-bold text-brand" title={pdf.filename}>
                      {pdf.filename}
                    </h3>
                    <p className="mt-1 text-xs text-text-muted">{formatBytes(pdf.size_bytes)}</p>
                    <p className="mt-1 text-[10px] text-violet">{documentTypeLabel(docType)}</p>
                    <div className="mt-auto pt-4">
                      <Button className="w-full" size="sm" onClick={() => openCreateModal(pdf)}>
                        <Plus className="h-4 w-4" />
                        Crear envío
                      </Button>
                    </div>
                  </CardBody>
                </Card>
              </motion.div>
            );
          })}
        </div>
      )}

      <CreateShipmentModal
        pdf={selectedPdf}
        open={modalOpen}
        loading={createMutation.isPending}
        onClose={() => {
          setModalOpen(false);
          setSelectedPdf(null);
        }}
        onConfirm={(payload) => void handleConfirmCreate(payload)}
      />
    </div>
  );
}
