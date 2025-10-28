from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class CreateLoanRequestDTO:
    """DTO para la solicitud de creación de un nuevo préstamo."""
    user_id: int
    book_id: int
    due_date: date