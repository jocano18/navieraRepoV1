import type { ShipmentStatus } from '@/types';

export const shipmentKeys = {
  all: ['shipments'] as const,
  lists: () => [...shipmentKeys.all, 'list'] as const,
  list: (status?: ShipmentStatus, skip?: number) =>
    [...shipmentKeys.lists(), { status, skip }] as const,
  details: () => [...shipmentKeys.all, 'detail'] as const,
  detail: (id: string) => [...shipmentKeys.details(), id] as const,
  extracted: (id: string) => [...shipmentKeys.detail(id), 'extracted'] as const,
  comparison: (id: string) => [...shipmentKeys.detail(id), 'comparison'] as const,
};
