import { Badge } from '@/components/ui';
import type { ShipmentStatus } from '@/types';

const STATUS_CONFIG: Record<
  ShipmentStatus,
  { label: string; tone: 'brand' | 'accent' | 'violet' | 'coral' | 'success' | 'muted' | 'cream' }
> = {
  PENDIENTE_EXTRACCION: { label: 'Pendiente extracción', tone: 'muted' },
  EXTRAIDO: { label: 'Extraído', tone: 'violet' },
  EN_DIGITACION: { label: 'En digitación', tone: 'violet' },
  EN_VALIDACION: { label: 'En validación', tone: 'cream' },
  INCOMPLETO: { label: 'Incompleto', tone: 'coral' },
  COMPLETO: { label: 'Completo', tone: 'success' },
  NOTIFICADO: { label: 'Notificado', tone: 'violet' },
  APROBADO_CLIENTE: { label: 'Aprobado cliente', tone: 'success' },
  CON_NOVEDAD: { label: 'Con novedad', tone: 'coral' },
  FINALIZADO: { label: 'Finalizado', tone: 'success' },
  RECHAZADO: { label: 'Rechazado', tone: 'accent' },
};

export function StatusBadge({ state }: { state: ShipmentStatus }) {
  const config = STATUS_CONFIG[state];
  return <Badge tone={config.tone}>{config.label}</Badge>;
}
