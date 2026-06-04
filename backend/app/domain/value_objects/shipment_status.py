"""Shipment status value object."""

from enum import Enum


class ShipmentStatus(str, Enum):
    """Lifecycle status of a shipment in the documentation workflow.

    See docs/state-machine.md for allowed transitions between states.
    """

    PENDIENTE_EXTRACCION = "PENDIENTE_EXTRACCION"
    EXTRAIDO = "EXTRAIDO"
    EN_DIGITACION = "EN_DIGITACION"
    EN_VALIDACION = "EN_VALIDACION"
    INCOMPLETO = "INCOMPLETO"
    COMPLETO = "COMPLETO"
    NOTIFICADO = "NOTIFICADO"
    APROBADO_CLIENTE = "APROBADO_CLIENTE"
    CON_NOVEDAD = "CON_NOVEDAD"
    FINALIZADO = "FINALIZADO"
    RECHAZADO = "RECHAZADO"
