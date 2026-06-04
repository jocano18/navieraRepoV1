import type { ComparisonResponse } from '@/types';

import { DiffField } from './DiffField';

export function ComparisonView({ comparison }: { comparison: ComparisonResponse }) {
  const mismatches = comparison.fields.filter((f) => !f.matches).length;

  return (
    <div className="space-y-4">
      <div
        className={
          comparison.is_complete
            ? 'rounded-lg bg-success-soft px-4 py-2 text-sm text-success'
            : 'rounded-lg border-l-4 border-l-coral bg-cream px-4 py-2 text-sm text-brand'
        }
      >
        {comparison.is_complete
          ? 'Todos los campos coinciden.'
          : `${String(mismatches)} campo(s) con diferencias.`}
      </div>
      <div className="max-h-[calc(100vh-280px)] space-y-2 overflow-y-auto pr-1">
        {comparison.fields.map((row) => (
          <DiffField key={row.field} row={row} />
        ))}
      </div>
    </div>
  );
}
