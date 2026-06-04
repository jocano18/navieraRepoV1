"""Application use cases."""

from app.application.use_cases.approve_shipment import ApproveShipmentUseCase
from app.application.use_cases.compare_data import CompareDataUseCase
from app.application.use_cases.correct_data import CorrectDataUseCase
from app.application.use_cases.create_shipment import CreateShipmentUseCase
from app.application.use_cases.extract_pdf_data import ExtractPdfDataUseCase
from app.application.use_cases.finalize_shipment import FinalizeShipmentUseCase
from app.application.use_cases.get_pdf_file import GetPdfFileUseCase
from app.application.use_cases.get_shipment import GetShipmentUseCase
from app.application.use_cases.list_inbox_pdfs import ListInboxPdfsUseCase
from app.application.use_cases.list_shipments import ListShipmentsUseCase
from app.application.use_cases.register_digitized_data import (
    RegisterDigitizedDataUseCase,
)
from app.application.use_cases.register_novelty import RegisterNoveltyUseCase
from app.application.use_cases.validate_and_transition import (
    ValidateAndTransitionUseCase,
)

__all__ = [
    "ApproveShipmentUseCase",
    "CompareDataUseCase",
    "CorrectDataUseCase",
    "CreateShipmentUseCase",
    "ExtractPdfDataUseCase",
    "FinalizeShipmentUseCase",
    "GetPdfFileUseCase",
    "GetShipmentUseCase",
    "ListInboxPdfsUseCase",
    "ListShipmentsUseCase",
    "RegisterDigitizedDataUseCase",
    "RegisterNoveltyUseCase",
    "ValidateAndTransitionUseCase",
]
