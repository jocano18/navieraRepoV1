import { create } from 'zustand';

import type { ShipmentStatus, UserRole } from '@/types';

export interface ToastItem {
  id: string;
  type: 'success' | 'error' | 'info';
  title: string;
  message?: string;
}

interface UiState {
  role: UserRole;
  shipmentStatusFilter: ShipmentStatus | 'ALL';
  shipmentSearch: string;
  toasts: ToastItem[];
  setRole: (role: UserRole) => void;
  setShipmentStatusFilter: (filter: ShipmentStatus | 'ALL') => void;
  setShipmentSearch: (search: string) => void;
  addToast: (toast: Omit<ToastItem, 'id'>) => void;
  removeToast: (id: string) => void;
}

let toastCounter = 0;

export const useUiStore = create<UiState>((set) => ({
  role: 'operator',
  shipmentStatusFilter: 'ALL',
  shipmentSearch: '',
  toasts: [],
  setRole: (role) => set({ role }),
  setShipmentStatusFilter: (shipmentStatusFilter) => set({ shipmentStatusFilter }),
  setShipmentSearch: (shipmentSearch) => set({ shipmentSearch }),
  addToast: (toast) =>
    set((state) => ({
      toasts: [
        ...state.toasts,
        { ...toast, id: `toast-${String(++toastCounter)}` },
      ],
    })),
  removeToast: (id) =>
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    })),
}));
