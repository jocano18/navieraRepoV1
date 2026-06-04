"""Cargo type value object."""

from enum import Enum


class CargoType(str, Enum):
    """Classification of cargo handling for PDF extraction strategy selection.

    Attributes:
        DIRECTO: Direct cargo — single consignee, dedicated extraction rules.
        CONSOLIDADO: Consolidated cargo — multiple consignees, grouped extraction.
    """

    DIRECTO = "DIRECTO"
    CONSOLIDADO = "CONSOLIDADO"
