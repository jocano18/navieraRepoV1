import { describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';

import { renderWithProviders } from '@/testing/render';

import { ShipmentsListPage } from './ShipmentsListPage';

describe('ShipmentsListPage', () => {
  it('renders shipments with correct status badges', async () => {
    renderWithProviders(<ShipmentsListPage />, { route: '/shipments' });

    await waitFor(() => {
      expect(screen.getByText('REF-001')).toBeInTheDocument();
    });

    expect(screen.getByText('En validación')).toBeInTheDocument();
    expect(screen.getByText('Completo')).toBeInTheDocument();
  });
});
