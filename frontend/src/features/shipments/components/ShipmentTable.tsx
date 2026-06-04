import { Link } from 'react-router-dom';
import { ArrowRight, FileText } from 'lucide-react';

import { Skeleton } from '@/components/ui';
import { formatDate } from '@/utils/format';
import type { ShipmentSummary } from '@/types';

import { StatusBadge } from './StatusBadge';

export function ShipmentTable({
  shipments,
  loading,
}: {
  shipments: ShipmentSummary[];
  loading?: boolean;
}) {
  if (loading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-14 w-full" />
        ))}
      </div>
    );
  }

  if (shipments.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-text-muted">
        No hay envíos que coincidan con el filtro.
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[640px] text-left text-sm">
        <thead>
          <tr className="border-b border-border text-xs uppercase tracking-wide text-text-muted">
            <th className="px-4 py-3 font-semibold">Referencia</th>
            <th className="px-4 py-3 font-semibold">PDF</th>
            <th className="px-4 py-3 font-semibold">Estado</th>
            <th className="px-4 py-3 font-semibold">Creado</th>
            <th className="px-4 py-3 font-semibold sr-only">Acciones</th>
          </tr>
        </thead>
        <tbody>
          {shipments.map((s) => (
            <tr
              key={s.id}
              className="border-b border-border/60 transition-colors hover:bg-lilac-soft/50"
            >
              <td className="px-4 py-3 font-semibold text-brand">{s.reference}</td>
              <td className="px-4 py-3">
                <span className="inline-flex items-center gap-1.5 text-text-muted">
                  <FileText className="h-4 w-4" aria-hidden />
                  {s.source_pdf_filename}
                </span>
              </td>
              <td className="px-4 py-3">
                <StatusBadge state={s.status} />
              </td>
              <td className="px-4 py-3 text-text-muted">{formatDate(s.created_at)}</td>
              <td className="px-4 py-3 text-right">
                <Link
                  to={`/shipments/${s.id}`}
                  className="inline-flex items-center gap-1 rounded-lg px-3 py-1.5 text-sm font-semibold text-violet hover:bg-lilac-soft"
                >
                  Abrir
                  <ArrowRight className="h-4 w-4" aria-hidden />
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
