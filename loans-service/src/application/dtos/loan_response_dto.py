from dataclasses import dataclass
from datetime import date
from uuid import UUID

@dataclass(frozen=True)
class LoanResponseDTO:
    """DTO para la respuesta exitosa de un préstamo."""
    loan_id: UUID
    user_id: int
    book_id: int
    loan_date: date
    due_date: date
    status: str