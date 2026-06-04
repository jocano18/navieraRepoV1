import { DashboardView } from '@/features/dashboard/components/DashboardView';
import { ShipmentTable, StatusBadge, useShipmentsList } from '@/features/shipments';
import { PIPELINE_STATUSES } from '@/utils/shipment-state';
import type { ShipmentStatus } from '@/types';

export function DashboardRoutePage() {
  const { data, isLoading } = useShipmentsList();

  const counts = PIPELINE_STATUSES.reduce(
    (acc, status) => {
      acc[status] = data?.filter((s) => s.status === status).length ?? 0;
      return acc;
    },
    {} as Record<ShipmentStatus, number>,
  );

  const recent = [...(data ?? [])]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 8);

  return (
    <DashboardView
      total={data?.length ?? 0}
      counts={counts}
      isLoading={isLoading}
      recentTable={<ShipmentTable shipments={recent} loading={isLoading} />}
      statusBadge={(status) => <StatusBadge state={status} />}
    />
  );
}
