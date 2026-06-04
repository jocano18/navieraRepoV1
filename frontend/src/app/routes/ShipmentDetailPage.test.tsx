import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { renderWithProviders } from '@/testing/render';
import { useUiStore } from '@/stores/ui-store';

import { ShipmentDetailPage } from './ShipmentDetailPage';

describe('ShipmentDetailPage', () => {
  it('disables mark complete when comparison has mismatches', async () => {
    useUiStore.setState({ role: 'executive' });
    renderWithProviders(<ShipmentDetailPage />, {
      route: '/shipments/11111111-1111-1111-1111-111111111111',
      path: '/shipments/:id',
    });

    await waitFor(() => {
      expect(screen.getByText('Marcar completo')).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: /Marcar completo/i })).toBeDisabled();
  });

  it('shows success toast after approve flow', async () => {
    useUiStore.setState({ role: 'executive' });
    const user = userEvent.setup();
    renderWithProviders(<ShipmentDetailPage />, {
      route: '/shipments/22222222-2222-2222-2222-222222222222',
      path: '/shipments/:id',
    });

    await waitFor(() => {
      expect(screen.getByText('Aprobar y notificar')).toBeInTheDocument();
    });

    await user.click(screen.getByRole('button', { name: /Aprobar y notificar/i }));
    await user.click(screen.getByRole('button', { name: /Confirmar envío/i }));

    await waitFor(() => {
      expect(screen.getByText('Cliente notificado')).toBeInTheDocument();
    });
  });
});
