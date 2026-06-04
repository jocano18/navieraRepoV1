import type { HTMLAttributes } from 'react';

import { cn } from '@/lib/cn';

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: 'brand' | 'accent' | 'violet' | 'coral' | 'success' | 'muted' | 'cream';
}

const tones: Record<NonNullable<BadgeProps['tone']>, string> = {
  brand: 'bg-brand text-white',
  accent: 'bg-accent text-white',
  violet: 'bg-violet/15 text-violet',
  coral: 'bg-coral/15 text-coral',
  success: 'bg-success-soft text-success',
  muted: 'bg-lilac-soft text-text-muted',
  cream: 'bg-cream text-brand',
};

export function Badge({ className, tone = 'muted', children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold',
        tones[tone],
        className,
      )}
      {...props}
    >
      {children}
    </span>
  );
}
