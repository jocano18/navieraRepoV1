import { Badge } from '@/components/ui';
import type { FieldSource } from '@/types';

const SOURCE_TONE: Record<FieldSource, 'success' | 'violet' | 'coral' | 'muted'> = {
  NATIVE: 'success',
  OCR: 'violet',
  NOT_FOUND: 'coral',
};

const SOURCE_LABEL: Record<FieldSource, string> = {
  NATIVE: 'Nativo',
  OCR: 'OCR',
  NOT_FOUND: 'No encontrado',
};

export function SourceTag({ source }: { source: FieldSource }) {
  return <Badge tone={SOURCE_TONE[source]}>{SOURCE_LABEL[source]}</Badge>;
}
