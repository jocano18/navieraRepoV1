import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';

import { renderWithProviders } from '@/testing/render';

import { StatusBadge } from './StatusBadge';

describe('StatusBadge', () => {
  it('renders COMPLETO with success label', () => {
    renderWithProviders(<StatusBadge state="COMPLETO" />);
    expect(screen.getByText('Completo')).toBeInTheDocument();
  });

  it('renders INCOMPLETO with attention label', () => {
    renderWithProviders(<StatusBadge state="INCOMPLETO" />);
    expect(screen.getByText('Incompleto')).toBeInTheDocument();
  });
});
