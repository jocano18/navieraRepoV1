import { useMemo } from 'react';
import { Package } from 'lucide-react';

import { Card, CardBody, CardHeader, EmptyState, Input } from '@/components/ui';
import { useUiStore } from '@/stores/ui-store';

import { useShipmentsList } from '../api/use-shipments';
import { ShipmentTable } from './ShipmentTable';
import { StatusFilterChips } from './StatusFilterChips';

export function ShipmentsListPage() {
  const filter = useUiStore((s) => s.shipmentStatusFilter);
  const setFilter = useUiStore((s) => s.setShipmentStatusFilter);
  const search = useUiStore((s) => s.shipmentSearch);
  const setSearch = useUiStore((s) => s.setShipmentSearch);

  const statusParam = filter === 'ALL' ? undefined : filter;
  const { data, isLoading, isError } = useShipmentsList(statusParam);

  const filtered = useMemo(() => {
    if (!data) return [];
    const q = search.trim().toLowerCase();
    if (!q) return data;
    return data.filter(
      (s) =>
        s.reference.toLowerCase().includes(q) ||
        s.source_pdf_filename.toLowerCase().includes(q),
    );
  }, [data, search]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-brand">Envíos</h1>
        <p className="mt-1 text-text-muted">
          Gestiona el flujo de documentación B/L desde extracción hasta notificación.
        </p>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <StatusFilterChips value={filter} onChange={setFilter} />
            <div className="w-full lg:max-w-xs">
              <Input
                placeholder="Buscar referencia o PDF…"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                aria-label="Buscar envíos"
              />
            </div>
          </div>
        </CardHeader>
        <CardBody>
          {isError ? (
            <p className="text-sm text-coral" role="alert">
              No se pudo cargar la lista de envíos.
            </p>
          ) : filtered.length === 0 && !isLoading ? (
            <EmptyState
              icon={Package}
              title="Sin envíos"
              description="Crea un envío desde la bandeja de entrada o ajusta los filtros."
            />
          ) : (
            <ShipmentTable shipments={filtered} loading={isLoading} />
          )}
        </CardBody>
      </Card>
    </div>
  );
}
