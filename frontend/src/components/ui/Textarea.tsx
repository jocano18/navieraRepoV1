import { forwardRef, type TextareaHTMLAttributes } from 'react';

import { cn } from '@/lib/cn';

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, id, ...props }, ref) => {
    const areaId = id ?? label?.toLowerCase().replace(/\s+/g, '-');
    return (
      <div className="flex flex-col gap-1.5">
        {label ? (
          <label htmlFor={areaId} className="text-sm font-medium text-brand">
            {label}
          </label>
        ) : null}
        <textarea
          ref={ref}
          id={areaId}
          className={cn(
            'min-h-[80px] rounded-lg border border-border bg-surface px-3 py-2 text-sm text-brand',
            'placeholder:text-text-muted focus:border-violet',
            error && 'border-coral',
            className,
          )}
          {...props}
        />
        {error ? <p className="text-xs text-coral">{error}</p> : null}
      </div>
    );
  },
);

Textarea.displayName = 'Textarea';
