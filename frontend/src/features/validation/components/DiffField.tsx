import { cn } from '@/lib/cn';
import { formatFieldLabel } from '@/utils/format';
import type { FieldComparison } from '@/types';

import { SourceTag } from './SourceTag';

export function DiffField({ row }: { row: FieldComparison }) {
  const mismatch = !row.matches;
  return (
    <div
      className={cn(
        'rounded-lg border-l-4 px-4 py-3 transition-colors',
        mismatch
          ? 'border-l-coral bg-cream'
          : 'border-l-transparent bg-lilac-soft/60',
      )}
      data-testid={`diff-field-${row.field}`}
      data-match={row.matches}
    >
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <span className="text-xs font-bold uppercase tracking-wide text-brand">
          {formatFieldLabel(row.field)}
        </span>
        <SourceTag source={row.source} />
      </div>
      <div className="grid gap-3 sm:grid-cols-2">
        <div>
          <p className="text-[10px] font-semibold uppercase text-text-muted">Extraído</p>
          <p className="text-sm text-brand">{row.extracted_value || '—'}</p>
        </div>
        <div>
          <p className="text-[10px] font-semibold uppercase text-text-muted">Digitado</p>
          <p className={cn('text-sm', mismatch ? 'font-semibold text-coral' : 'text-brand')}>
            {row.typed_value || '—'}
          </p>
        </div>
      </div>
    </div>
  );
}
