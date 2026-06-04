import { cn } from '@/lib/cn';
import type { ShipmentStatus } from '@/types';

import { StatusBadge } from './StatusBadge';

const FILTER_STATUSES: (ShipmentStatus | 'ALL')[] = [
  'ALL',
  'PENDIENTE_EXTRACCION',
  'EN_DIGITACION',
  'EN_VALIDACION',
  'INCOMPLETO',
  'COMPLETO',
  'NOTIFICADO',
  'FINALIZADO',
];

export function StatusFilterChips({
  value,
  onChange,
}: {
  value: ShipmentStatus | 'ALL';
  onChange: (v: ShipmentStatus | 'ALL') => void;
}) {
  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label="Filtrar por estado">
      {FILTER_STATUSES.map((status) => (
        <button
          key={status}
          type="button"
          onClick={() => onChange(status)}
          className={cn(
            'rounded-full border px-3 py-1 transition-all',
            value === status
              ? 'border-accent bg-cream shadow-sm'
              : 'border-border bg-surface hover:border-violet',
          )}
        >
          {status === 'ALL' ? (
            <span className="text-xs font-semibold text-brand">Todos</span>
          ) : (
            <StatusBadge state={status} />
          )}
        </button>
      ))}
    </div>
  );
}
