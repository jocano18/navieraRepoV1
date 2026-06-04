import { Link } from 'react-router-dom';
import { ArrowRight, BarChart3, Layers } from 'lucide-react';
import { motion } from 'framer-motion';
import type { ReactNode } from 'react';

import { Card, CardBody, CardHeader } from '@/components/ui';
import { PIPELINE_STATUSES } from '@/utils/shipment-state';
import type { ShipmentStatus } from '@/types';

export interface DashboardViewProps {
  total: number;
  counts: Record<ShipmentStatus, number>;
  isLoading: boolean;
  recentTable: ReactNode;
  statusBadge: (status: ShipmentStatus) => ReactNode;
}

export function DashboardView({
  total,
  counts,
  isLoading,
  recentTable,
  statusBadge,
}: DashboardViewProps) {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-extrabold tracking-tight text-brand">Dashboard</h1>
        <p className="mt-1 text-text-muted">
          Vista general del pipeline de documentación B/L.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <SummaryCard
          icon={BarChart3}
          label="Total envíos"
          value={isLoading ? '—' : String(total)}
          accent
        />
        <SummaryCard
          icon={Layers}
          label="En validación"
          value={isLoading ? '—' : String(counts.EN_VALIDACION)}
        />
        <SummaryCard label="Completos" value={isLoading ? '—' : String(counts.COMPLETO)} />
        <SummaryCard
          label="Finalizados"
          value={isLoading ? '—' : String(counts.FINALIZADO)}
        />
      </div>

      <Card>
        <CardHeader>
          <h2 className="text-lg font-bold text-brand">Pipeline de estados</h2>
        </CardHeader>
        <CardBody>
          <div className="flex gap-3 overflow-x-auto pb-2">
            {PIPELINE_STATUSES.map((status, i) => (
              <motion.div
                key={status}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.03 }}
                className="min-w-[140px] flex-shrink-0 rounded-xl border border-border bg-surface p-4 text-center shadow-soft"
              >
                <p className="text-2xl font-extrabold text-brand">
                  {isLoading ? '…' : counts[status]}
                </p>
                <div className="mt-2 flex justify-center">{statusBadge(status)}</div>
              </motion.div>
            ))}
          </div>
        </CardBody>
      </Card>

      <Card>
        <CardHeader className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-brand">Envíos recientes</h2>
          <Link
            to="/shipments"
            className="inline-flex items-center gap-1 text-sm font-semibold text-violet hover:underline"
          >
            Ver todos
            <ArrowRight className="h-4 w-4" aria-hidden />
          </Link>
        </CardHeader>
        <CardBody>{recentTable}</CardBody>
      </Card>
    </div>
  );
}

function SummaryCard({
  icon: Icon,
  label,
  value,
  accent,
}: {
  icon?: typeof BarChart3;
  label: string;
  value: string;
  accent?: boolean;
}) {
  return (
    <Card
      className={
        accent ? 'border-accent/30 bg-gradient-to-br from-cream/80 to-surface' : undefined
      }
    >
      <CardBody className="flex items-start gap-3">
        {Icon ? (
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand text-accent">
            <Icon className="h-5 w-5" aria-hidden />
          </div>
        ) : null}
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-text-muted">
            {label}
          </p>
          <p className="text-3xl font-extrabold text-brand">{value}</p>
        </div>
      </CardBody>
    </Card>
  );
}
