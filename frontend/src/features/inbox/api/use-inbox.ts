import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { createShipmentFromInbox, fetchInboxPdfs } from './inbox-api';

export const inboxKeys = {
  all: ['inbox'] as const,
  pdfs: () => [...inboxKeys.all, 'pdfs'] as const,
};

const shipmentsListKey = ['shipments', 'list'] as const;

export function useInboxPdfs() {
  return useQuery({
    queryKey: inboxKeys.pdfs(),
    queryFn: fetchInboxPdfs,
  });
}

export function useCreateShipmentFromInbox() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createShipmentFromInbox,
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: shipmentsListKey });
    },
  });
}
