import { AnimatePresence, motion } from 'framer-motion';
import { CheckCircle2, AlertCircle, Info } from 'lucide-react';
import { useEffect } from 'react';

import { cn } from '@/lib/cn';
import { useUiStore, type ToastItem } from '@/stores/ui-store';

const icons = {
  success: CheckCircle2,
  error: AlertCircle,
  info: Info,
};

function ToastCard({ toast }: { toast: ToastItem }) {
  const remove = useUiStore((s) => s.removeToast);
  const Icon = icons[toast.type];

  useEffect(() => {
    const t = setTimeout(() => remove(toast.id), 5000);
    return () => clearTimeout(t);
  }, [toast.id, remove]);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: 24 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 24 }}
      className={cn(
        'flex w-80 gap-3 rounded-xl border border-border bg-surface p-4 shadow-elevated',
        toast.type === 'success' && 'border-l-4 border-l-success',
        toast.type === 'error' && 'border-l-4 border-l-coral',
        toast.type === 'info' && 'border-l-4 border-l-violet',
      )}
      role="status"
    >
      <Icon
        className={cn(
          'h-5 w-5 shrink-0',
          toast.type === 'success' && 'text-success',
          toast.type === 'error' && 'text-coral',
          toast.type === 'info' && 'text-violet',
        )}
        aria-hidden
      />
      <div>
        <p className="text-sm font-semibold text-brand">{toast.title}</p>
        {toast.message ? (
          <p className="mt-0.5 text-xs text-text-muted">{toast.message}</p>
        ) : null}
      </div>
    </motion.div>
  );
}

export function ToastRegion() {
  const toasts = useUiStore((s) => s.toasts);
  return (
    <div
      className="pointer-events-none fixed right-4 top-4 z-[100] flex flex-col gap-2"
      aria-live="polite"
    >
      <AnimatePresence mode="popLayout">
        {toasts.map((t) => (
          <div key={t.id} className="pointer-events-auto">
            <ToastCard toast={t} />
          </div>
        ))}
      </AnimatePresence>
    </div>
  );
}
