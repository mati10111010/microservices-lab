from dataclasses import dataclass
from datetime import date
from typing import Optional
from uuid import UUID

# DTO de entrada para el caso de uso
@dataclass
class LoanRequestDTO:
    user_id: str # Asumimos UUID como str en el input
    book_id: str
    days: int

# DTO de respuesta para el caso de uso
@dataclass
class LoanResponseDTO:
    loan_id: UUID
    user_id: str
    book_id: str
    start_date: date
    due_date: date
    status: str

# Entidad del Dominio (Pura)
@dataclass
class Loan:
    id: UUID
    user_id: str
    book_id: str
    start_date: date
    due_date: date
    status: str = "active"

    @classmethod
    def create(
        cls, id: UUID, user_id: str, book_id: str, start_date: date, days: int
    ) -> 'Loan':
        # Calcula la fecha de vencimiento (due_date)
        due_date = start_date.replace(day=start_date.day + days)
        return cls(
            id=id,
            user_id=user_id,
            book_id=book_id,
            start_date=start_date,
            due_date=due_date,
            status="active",
        )