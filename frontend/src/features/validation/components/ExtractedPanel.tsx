import { formatFieldLabel } from '@/utils/format';
import type { DocumentData } from '@/types';
import { BL_FIELD_KEYS } from '@/types';

import { SourceTag } from './SourceTag';

export function ExtractedPanel({ data }: { data: DocumentData }) {
  const notFoundCount = BL_FIELD_KEYS.filter((k) => data[k].source === 'NOT_FOUND').length;

  return (
    <div className="space-y-3">
      {notFoundCount > 0 ? (
        <p className="rounded-lg bg-cream/80 px-3 py-2 text-xs text-text-muted">
          {notFoundCount} campo(s) sin detectar automáticamente. Revisa el PDF y complétalos en
          digitación. Los B/L escaneados o en otro idioma pueden requerir OCR o ajuste de plantilla.
        </p>
      ) : null}
      {BL_FIELD_KEYS.map((key) => {
        const field = data[key];
        return (
          <div
            key={key}
            className="rounded-lg border border-border bg-surface px-4 py-3"
          >
            <div className="mb-1 flex items-center justify-between gap-2">
              <span className="text-xs font-bold uppercase text-text-muted">
                {formatFieldLabel(key)}
              </span>
              <SourceTag source={field.source} />
            </div>
            <p className="text-sm text-brand">{field.value || '—'}</p>
          </div>
        );
      })}
      {data.freight_terms ? (
        <div className="rounded-lg border border-border px-4 py-3">
          <span className="text-xs font-bold uppercase text-text-muted">Freight terms</span>
          <p className="text-sm text-brand">{data.freight_terms}</p>
        </div>
      ) : null}
      {data.containers.length > 0 ? (
        <ContainersReadOnly containers={data.containers} />
      ) : null}
    </div>
  );
}

function ContainersReadOnly({
  containers,
}: {
  containers: DocumentData['containers'];
}) {
  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full text-left text-xs">
        <thead className="bg-lilac-soft text-text-muted">
          <tr>
            <th className="px-3 py-2">Contenedor</th>
            <th className="px-3 py-2">Sello</th>
            <th className="px-3 py-2">Tipo</th>
            <th className="px-3 py-2">Bultos</th>
          </tr>
        </thead>
        <tbody>
          {containers.map((c, i) => (
            <tr key={i} className="border-t border-border">
              <td className="px-3 py-2">{c.container_number}</td>
              <td className="px-3 py-2">{c.seal}</td>
              <td className="px-3 py-2">{c.container_type}</td>
              <td className="px-3 py-2">{c.packages}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
