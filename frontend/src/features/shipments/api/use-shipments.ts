import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import type { DigitizedPayload, ShipmentStatus } from '@/types';

import {
  approveShipment,
  correctDigitized,
  createShipment,
  extractShipment,
  fetchComparison,
  fetchShipment,
  fetchShipments,
  registerDigitized,
  registerNovelty,
  validateShipment,
} from './shipments-api';
import { shipmentKeys } from './keys';

export function useShipmentsList(status?: ShipmentStatus, skip = 0) {
  return useQuery({
    queryKey: shipmentKeys.list(status, skip),
    queryFn: () => fetchShipments({ status, skip, limit: 100 }),
  });
}

export function useShipment(id: string | undefined) {
  return useQuery({
    queryKey: shipmentKeys.detail(id ?? ''),
    queryFn: () => fetchShipment(id!),
    enabled: Boolean(id),
  });
}

export function useComparison(id: string | undefined, enabled = true) {
  return useQuery({
    queryKey: shipmentKeys.comparison(id ?? ''),
    queryFn: () => fetchComparison(id!),
    enabled: Boolean(id) && enabled,
  });
}

export function useCreateShipment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createShipment,
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}

export function useExtractShipment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: extractShipment,
    onSuccess: (data, id) => {
      qc.setQueryData(shipmentKeys.extracted(id), data);
      void qc.invalidateQueries({ queryKey: shipmentKeys.detail(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}

export function useRegisterDigitized() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: DigitizedPayload }) =>
      registerDigitized(id, payload),
    onSuccess: (_, { id }) => {
      void qc.invalidateQueries({ queryKey: shipmentKeys.detail(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.comparison(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}

export function useCorrectDigitized() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: DigitizedPayload }) =>
      correctDigitized(id, payload),
    onSuccess: (_, { id }) => {
      void qc.invalidateQueries({ queryKey: shipmentKeys.detail(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.comparison(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}

export function useValidateShipment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, markComplete }: { id: string; markComplete: boolean }) =>
      validateShipment(id, markComplete),
    onSuccess: (_, { id }) => {
      void qc.invalidateQueries({ queryKey: shipmentKeys.detail(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.comparison(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}

export function useApproveShipment() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: approveShipment,
    onSuccess: (_, id) => {
      void qc.invalidateQueries({ queryKey: shipmentKeys.detail(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}

export function useRegisterNovelty() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, description }: { id: string; description: string }) =>
      registerNovelty(id, description),
    onSuccess: (_, { id }) => {
      void qc.invalidateQueries({ queryKey: shipmentKeys.detail(id) });
      void qc.invalidateQueries({ queryKey: shipmentKeys.lists() });
    },
  });
}
