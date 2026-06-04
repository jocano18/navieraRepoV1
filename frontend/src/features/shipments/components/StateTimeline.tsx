import { Check } from 'lucide-react';

import { cn } from '@/lib/cn';
import { PIPELINE_STATUSES } from '@/utils/shipment-state';
import type { ShipmentStatus } from '@/types';

import { StatusBadge } from './StatusBadge';

const STEP_LABELS: Partial<Record<ShipmentStatus, string>> = {
  PENDIENTE_EXTRACCION: 'Extracción',
  EXTRAIDO: 'Extraído',
  EN_DIGITACION: 'Digitación',
  EN_VALIDACION: 'Validación',
  INCOMPLETO: 'Corrección',
  COMPLETO: 'Completo',
  NOTIFICADO: 'Notificado',
  APROBADO_CLIENTE: 'Cliente',
  FINALIZADO: 'Finalizado',
};

export function StateTimeline({ current }: { current: ShipmentStatus }) {
  const currentIndex = PIPELINE_STATUSES.indexOf(current);

  if (current === 'INCOMPLETO' || current === 'CON_NOVEDAD' || current === 'RECHAZADO') {
    return (
      <div className="flex flex-wrap items-center gap-3">
        <StatusBadge state={current} />
        <p className="text-sm text-text-muted">
          {current === 'INCOMPLETO'
            ? 'Requiere corrección del operador antes de revalidar.'
            : current === 'CON_NOVEDAD'
              ? 'Novedad registrada — vuelve a validación.'
              : 'Envío rechazado.'}
        </p>
      </div>
    );
  }

  return (
    <ol className="flex flex-wrap gap-2" aria-label="Progreso del envío">
      {PIPELINE_STATUSES.map((step, index) => {
        const done = index < currentIndex;
        const active = step === current;
        const upcoming = index > currentIndex;
        return (
          <li
            key={step}
            className={cn(
              'flex items-center gap-2 rounded-xl border px-3 py-2 text-xs font-semibold transition-colors',
              done && 'border-success/30 bg-success-soft text-success',
              active && 'border-accent bg-cream text-brand shadow-sm',
              upcoming && 'border-border bg-surface text-text-muted',
            )}
          >
            <span
              className={cn(
                'flex h-5 w-5 items-center justify-center rounded-full text-[10px]',
                done && 'bg-success text-white',
                active && 'bg-accent text-white',
                upcoming && 'bg-lilac-soft text-text-muted',
              )}
              aria-hidden
            >
              {done ? <Check className="h-3 w-3" /> : index + 1}
            </span>
            {STEP_LABELS[step] ?? step}
          </li>
        );
      })}
    </ol>
  );
}
