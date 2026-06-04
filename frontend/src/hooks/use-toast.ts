import { useCallback } from 'react';

import { useUiStore } from '@/stores/ui-store';

export function useToast() {
  const addToast = useUiStore((s) => s.addToast);

  return {
    success: useCallback(
      (title: string, message?: string) => addToast({ type: 'success', title, message }),
      [addToast],
    ),
    error: useCallback(
      (title: string, message?: string) => addToast({ type: 'error', title, message }),
      [addToast],
    ),
    info: useCallback(
      (title: string, message?: string) => addToast({ type: 'info', title, message }),
      [addToast],
    ),
  };
}
