import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { AlertTriangle, CheckCircle2, Save, Sparkles } from 'lucide-react';

import {
  Button,
  Card,
  CardBody,
  Skeleton,
  TabList,
  TabPanel,
  Tabs,
  TabTrigger,
} from '@/components/ui';
import { ApproveNotifyModal } from '@/features/notifications';
import {
  ComparisonView,
  ExtractedPanel,
  PdfViewer,
  TypedForm,
} from '@/features/validation';
import {
  shipmentKeys,
  StateTimeline,
  StatusBadge,
  useApproveShipment,
  useComparison,
  useCorrectDigitized,
  useExtractShipment,
  useRegisterDigitized,
  useShipment,
  useValidateShipment,
} from '@/features/shipments';
import { useToast } from '@/hooks/use-toast';
import { useUiStore } from '@/stores/ui-store';
import type { DigitizedPayload, DocumentData } from '@/types';
import {
  digitizedFromDocument,
  emptyDigitizedPayload,
} from '@/utils/document-data';
import {
  canApprove,
  canCompare,
  canEditDigitized,
  canExtract,
  canValidate,
} from '@/utils/shipment-state';

export function ShipmentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const shipmentId = id ?? '';
  const role = useUiStore((s) => s.role);
  const toast = useToast();
  const qc = useQueryClient();

  const { data: shipment, isLoading } = useShipment(shipmentId);
  const extracted = qc.getQueryData<DocumentData>(shipmentKeys.extracted(shipmentId));
  const extractMutation = useExtractShipment();
  const registerMutation = useRegisterDigitized();
  const correctMutation = useCorrectDigitized();
  const validateMutation = useValidateShipment();
  const approveMutation = useApproveShipment();

  const showComparison = shipment ? canCompare(shipment.status) : false;
  const { data: comparison, isLoading: comparisonLoading } = useComparison(
    shipmentId,
    showComparison,
  );

  const [digitized, setDigitized] = useState<DigitizedPayload>(emptyDigitizedPayload());
  const [approveOpen, setApproveOpen] = useState(false);

  useEffect(() => {
    if (shipment?.extracted_data) {
      qc.setQueryData(shipmentKeys.extracted(shipmentId), shipment.extracted_data);
    }
  }, [shipment, shipmentId, qc]);

  useEffect(() => {
    if (extracted) {
      setDigitized(digitizedFromDocument(extracted));
    } else if (comparison) {
      const fields = Object.fromEntries(
        comparison.fields.map((f) => [f.field, f.typed_value]),
      );
      setDigitized((prev) => ({ ...prev, fields: { ...prev.fields, ...fields } }));
    }
  }, [extracted, comparison]);

  if (isLoading || !shipment) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-10 w-64" />
        <Skeleton className="h-[500px] w-full" />
      </div>
    );
  }

  const editable = canEditDigitized(shipment.status, role);
  const validating = canValidate(shipment.status, role);
  const approvable = canApprove(shipment.status, role);

  const handleExtract = async () => {
    try {
      await extractMutation.mutateAsync(shipmentId);
      toast.success('Extracción completada', 'Los datos del B/L están listos para digitación.');
    } catch {
      toast.error('Error en extracción', 'No se pudo procesar el PDF.');
    }
  };

  const handleSaveDigitized = async () => {
    try {
      if (shipment.status === 'INCOMPLETO') {
        await correctMutation.mutateAsync({ id: shipmentId, payload: digitized });
        toast.success('Datos corregidos', 'El envío volvió a validación.');
      } else {
        await registerMutation.mutateAsync({ id: shipmentId, payload: digitized });
        toast.success('Datos registrados', 'Enviado a validación ejecutiva.');
      }
    } catch {
      toast.error('Error al guardar', 'Verifica los campos e intenta de nuevo.');
    }
  };

  const handleValidate = async (markComplete: boolean) => {
    try {
      const result = await validateMutation.mutateAsync({
        id: shipmentId,
        markComplete,
      });
      toast.success(
        markComplete ? 'Marcado completo' : 'Marcado incompleto',
        `Nuevo estado: ${result.new_status}`,
      );
    } catch {
      toast.error('Validación fallida');
    }
  };

  const handleApprove = async () => {
    try {
      await approveMutation.mutateAsync(shipmentId);
      setApproveOpen(false);
      toast.success('Cliente notificado', 'El envío fue aprobado y notificado correctamente.');
    } catch {
      toast.error('No se pudo aprobar', 'Verifica que el envío esté en estado COMPLETO.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-2xl font-extrabold text-brand">{shipment.reference}</h1>
            <StatusBadge state={shipment.status} />
          </div>
          <p className="mt-1 text-sm text-text-muted">{shipment.source_pdf_filename}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {canExtract(shipment.status) && role === 'operator' ? (
            <Button loading={extractMutation.isPending} onClick={() => void handleExtract()}>
              <Sparkles className="h-4 w-4" />
              Extraer PDF
            </Button>
          ) : null}
          {editable ? (
            <Button
              variant="secondary"
              loading={registerMutation.isPending || correctMutation.isPending}
              onClick={() => void handleSaveDigitized()}
            >
              <Save className="h-4 w-4" />
              Guardar digitación
            </Button>
          ) : null}
          {validating ? (
            <>
              <Button
                variant="outline"
                loading={validateMutation.isPending}
                onClick={() => void handleValidate(false)}
              >
                <AlertTriangle className="h-4 w-4" />
                Marcar incompleto
              </Button>
              <Button
                loading={validateMutation.isPending}
                disabled={comparison ? !comparison.is_complete : true}
                onClick={() => void handleValidate(true)}
              >
                <CheckCircle2 className="h-4 w-4" />
                Marcar completo
              </Button>
            </>
          ) : null}
          {approvable ? (
            <Button onClick={() => setApproveOpen(true)}>Aprobar y notificar</Button>
          ) : null}
        </div>
      </div>

      <StateTimeline current={shipment.status} />

      <div className="grid gap-6 xl:grid-cols-2">
        <PdfViewer shipmentId={shipmentId} />
        <Card className="min-h-[480px]">
          <CardBody>
            <Tabs defaultValue="extracted">
              <TabList>
                <TabTrigger value="extracted">Extraído</TabTrigger>
                <TabTrigger value="typed">Digitado</TabTrigger>
                <TabTrigger value="comparison">Comparación</TabTrigger>
              </TabList>
              <TabPanel value="extracted">
                {extracted ? (
                  <ExtractedPanel data={extracted} />
                ) : (
                  <p className="py-8 text-center text-sm text-text-muted">
                    Ejecuta la extracción para ver los campos del B/L.
                  </p>
                )}
              </TabPanel>
              <TabPanel value="typed">
                <TypedForm value={digitized} onChange={setDigitized} disabled={!editable} />
              </TabPanel>
              <TabPanel value="comparison">
                {comparisonLoading ? (
                  <Skeleton className="h-40 w-full" />
                ) : comparison ? (
                  <ComparisonView comparison={comparison} />
                ) : (
                  <p className="py-8 text-center text-sm text-text-muted">
                    La comparación estará disponible tras registrar la digitación.
                  </p>
                )}
              </TabPanel>
            </Tabs>
          </CardBody>
        </Card>
      </div>

      <ApproveNotifyModal
        open={approveOpen}
        onClose={() => setApproveOpen(false)}
        reference={shipment.reference}
        loading={approveMutation.isPending}
        onConfirm={() => void handleApprove()}
      />
    </div>
  );
}
