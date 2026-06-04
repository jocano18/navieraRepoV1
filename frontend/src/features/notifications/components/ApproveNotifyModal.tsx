import { Mail, User } from 'lucide-react';

import { Button, Modal } from '@/components/ui';
import { DEMO_CLIENT } from '@/types';

export interface ApproveNotifyModalProps {
  open: boolean;
  onClose: () => void;
  reference: string;
  loading?: boolean;
  onConfirm: () => void;
}

export function ApproveNotifyModal({
  open,
  onClose,
  reference,
  loading,
  onConfirm,
}: ApproveNotifyModalProps) {
  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Aprobar y notificar cliente"
      description={`Se enviará la confirmación del envío ${reference} al cliente registrado.`}
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancelar
          </Button>
          <Button loading={loading} onClick={onConfirm}>
            Confirmar envío
          </Button>
        </>
      }
    >
      <div className="space-y-4 rounded-xl bg-lilac-soft p-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-violet/15 text-violet">
            <User className="h-5 w-5" aria-hidden />
          </div>
          <div>
            <p className="font-semibold text-brand">{DEMO_CLIENT.name}</p>
            <p className="text-xs text-text-muted">NIT {DEMO_CLIENT.nit}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 text-sm text-brand">
          <Mail className="h-4 w-4 text-violet" aria-hidden />
          {DEMO_CLIENT.email}
        </div>
      </div>
      <p className="mt-4 text-xs text-text-muted">
        Al confirmar, el envío pasará a estado NOTIFICADO y se disparará el correo al cliente.
      </p>
    </Modal>
  );
}
