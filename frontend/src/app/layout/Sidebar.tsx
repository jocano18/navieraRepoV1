import { NavLink } from 'react-router-dom';
import { Inbox, LayoutDashboard, Package, Ship } from 'lucide-react';

import { cn } from '@/lib/cn';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/inbox', label: 'Bandeja', icon: Inbox },
  { to: '/shipments', label: 'Envíos', icon: Package },
];

export function Sidebar() {
  return (
    <aside className="flex w-64 flex-col border-r border-border bg-brand text-white">
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-accent">
          <Ship className="h-5 w-5" aria-hidden />
        </div>
        <div>
          <p className="text-xs font-medium text-lilac">Naviera</p>
          <p className="text-lg font-extrabold leading-tight">Docs</p>
        </div>
      </div>
      <nav className="flex flex-1 flex-col gap-1 px-3" aria-label="Principal">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-semibold transition-all',
                isActive
                  ? 'bg-accent text-white shadow-md'
                  : 'text-lilac hover:bg-white/10 hover:text-white',
              )
            }
          >
            <Icon className="h-5 w-5 shrink-0" aria-hidden />
            {label}
          </NavLink>
        ))}
      </nav>
      <p className="px-6 py-4 text-[10px] text-lilac">Documentación B/L · v0.1</p>
    </aside>
  );
}
