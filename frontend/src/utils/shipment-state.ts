import type { ShipmentStatus, UserRole } from '@/types';

const ALLOWED: Record<ShipmentStatus, ShipmentStatus[]> = {
  PENDIENTE_EXTRACCION: ['EXTRAIDO'],
  EXTRAIDO: ['EN_DIGITACION'],
  EN_DIGITACION: ['EN_VALIDACION'],
  EN_VALIDACION: ['INCOMPLETO', 'COMPLETO'],
  INCOMPLETO: ['EN_VALIDACION'],
  COMPLETO: ['NOTIFICADO'],
  NOTIFICADO: ['APROBADO_CLIENTE'],
  APROBADO_CLIENTE: ['CON_NOVEDAD', 'FINALIZADO'],
  CON_NOVEDAD: ['EN_VALIDACION'],
  FINALIZADO: [],
  RECHAZADO: [],
};

export const PIPELINE_STATUSES: ShipmentStatus[] = [
  'PENDIENTE_EXTRACCION',
  'EXTRAIDO',
  'EN_DIGITACION',
  'EN_VALIDACION',
  'INCOMPLETO',
  'COMPLETO',
  'NOTIFICADO',
  'APROBADO_CLIENTE',
  'FINALIZADO',
];

export function canTransition(from: ShipmentStatus, to: ShipmentStatus): boolean {
  return ALLOWED[from]?.includes(to) ?? false;
}

export function canExtract(status: ShipmentStatus): boolean {
  return status === 'PENDIENTE_EXTRACCION';
}

export function canEditDigitized(status: ShipmentStatus, role: UserRole): boolean {
  if (role !== 'operator') return false;
  return ['EXTRAIDO', 'EN_DIGITACION', 'INCOMPLETO'].includes(status);
}

export function canValidate(status: ShipmentStatus, role: UserRole): boolean {
  return role === 'executive' && status === 'EN_VALIDACION';
}

export function canApprove(status: ShipmentStatus, role: UserRole): boolean {
  return role === 'executive' && status === 'COMPLETO';
}

export function canCompare(status: ShipmentStatus): boolean {
  return [
    'EN_VALIDACION',
    'INCOMPLETO',
    'COMPLETO',
    'NOTIFICADO',
    'APROBADO_CLIENTE',
    'CON_NOVEDAD',
    'FINALIZADO',
  ].includes(status);
}
