import { Plus, Trash2 } from 'lucide-react';

import { Button, Input, Textarea } from '@/components/ui';
import { formatFieldLabel } from '@/utils/format';
import { emptyContainer } from '@/utils/document-data';
import type { Container, DigitizedPayload } from '@/types';
import { BL_FIELD_KEYS } from '@/types';

export function TypedForm({
  value,
  onChange,
  disabled,
}: {
  value: DigitizedPayload;
  onChange: (v: DigitizedPayload) => void;
  disabled?: boolean;
}) {
  const updateField = (key: string, fieldValue: string) => {
    onChange({
      ...value,
      fields: { ...value.fields, [key]: fieldValue },
    });
  };

  const updateContainer = (index: number, patch: Partial<Container>) => {
    const containers = value.containers.map((c, i) =>
      i === index ? { ...c, ...patch } : c,
    );
    onChange({ ...value, containers });
  };

  const addContainer = () => {
    onChange({ ...value, containers: [...value.containers, emptyContainer()] });
  };

  const removeContainer = (index: number) => {
    onChange({ ...value, containers: value.containers.filter((_, i) => i !== index) });
  };

  return (
    <div className="space-y-4">
      {BL_FIELD_KEYS.map((key) => {
        const isLong = key === 'description_of_goods' || key === 'marks_and_numbers';
        const label = formatFieldLabel(key);
        if (isLong) {
          return (
            <Textarea
              key={key}
              label={label}
              value={value.fields[key] ?? ''}
              disabled={disabled}
              onChange={(e) => updateField(key, e.target.value)}
            />
          );
        }
        return (
          <Input
            key={key}
            label={label}
            value={value.fields[key] ?? ''}
            disabled={disabled}
            onChange={(e) => updateField(key, e.target.value)}
          />
        );
      })}
      <Input
        label="Freight terms"
        value={value.freight_terms ?? ''}
        disabled={disabled}
        onChange={(e) =>
          onChange({ ...value, freight_terms: e.target.value || null })
        }
      />
      <div>
        <div className="mb-2 flex items-center justify-between">
          <h4 className="text-sm font-bold text-brand">Contenedores</h4>
          <Button
            type="button"
            variant="outline"
            size="sm"
            disabled={disabled}
            onClick={addContainer}
          >
            <Plus className="h-4 w-4" />
            Agregar
          </Button>
        </div>
        {value.containers.length === 0 ? (
          <p className="text-xs text-text-muted">Sin contenedores registrados.</p>
        ) : (
          <div className="space-y-3">
            {value.containers.map((c, index) => (
              <div
                key={index}
                className="grid gap-2 rounded-lg border border-border p-3 sm:grid-cols-2"
              >
                <Input
                  label="Número"
                  value={c.container_number}
                  disabled={disabled}
                  onChange={(e) =>
                    updateContainer(index, { container_number: e.target.value })
                  }
                />
                <Input
                  label="Sello"
                  value={c.seal}
                  disabled={disabled}
                  onChange={(e) => updateContainer(index, { seal: e.target.value })}
                />
                <Input
                  label="Tipo"
                  value={c.container_type}
                  disabled={disabled}
                  onChange={(e) =>
                    updateContainer(index, { container_type: e.target.value })
                  }
                />
                <Input
                  label="Bultos"
                  value={c.packages}
                  disabled={disabled}
                  onChange={(e) => updateContainer(index, { packages: e.target.value })}
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="sm:col-span-2"
                  disabled={disabled}
                  onClick={() => removeContainer(index)}
                >
                  <Trash2 className="h-4 w-4" />
                  Eliminar
                </Button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
