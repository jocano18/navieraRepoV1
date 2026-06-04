import { Briefcase, UserCog } from 'lucide-react';

import { cn } from '@/lib/cn';
import { useUiStore } from '@/stores/ui-store';
import type { UserRole } from '@/types';

const roles: { id: UserRole; label: string; icon: typeof UserCog }[] = [
  { id: 'operator', label: 'Operador', icon: UserCog },
  { id: 'executive', label: 'Ejecutivo', icon: Briefcase },
];

export function Topbar() {
  const role = useUiStore((s) => s.role);
  const setRole = useUiStore((s) => s.setRole);

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-surface px-6">
      <p className="text-sm text-text-muted">
        Rol activo:{' '}
        <span className="font-semibold text-brand">
          {role === 'operator' ? 'Operador' : 'Ejecutivo'}
        </span>
      </p>
      <div
        className="flex rounded-xl border border-border bg-lilac-soft p-1"
        role="group"
        aria-label="Cambiar rol"
      >
        {roles.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => setRole(id)}
            className={cn(
              'inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition-all',
              role === id ? 'bg-accent text-white shadow-sm' : 'text-text-muted hover:text-brand',
            )}
            aria-pressed={role === id}
          >
            <Icon className="h-4 w-4" aria-hidden />
            {label}
          </button>
        ))}
      </div>
    </header>
  );
}
