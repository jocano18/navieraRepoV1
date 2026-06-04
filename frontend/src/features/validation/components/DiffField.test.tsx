import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';

import { renderWithProviders } from '@/testing/render';

import { DiffField } from './DiffField';

describe('DiffField', () => {
  it('highlights mismatched field with data-match false', () => {
    renderWithProviders(
      <DiffField
        row={{
          field: 'bl_number',
          extracted_value: 'BL-1',
          typed_value: 'BL-2',
          matches: false,
          source: 'NATIVE',
        }}
      />,
    );
    const el = screen.getByTestId('diff-field-bl_number');
    expect(el).toHaveAttribute('data-match', 'false');
    expect(el.className).toMatch(/bg-cream/);
    expect(el.className).toMatch(/border-l-coral/);
  });
});
