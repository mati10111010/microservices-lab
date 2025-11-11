from abc import ABC, abstractmethod
from uuid import UUID
from ..entities.loan import Loan
class LoansRepository(ABC):
    """Puerto de persistencia para la entidad Loan."""
    @abstractmethod
    def save(self, loan: Loan) -> Loan:
        """Guarda o actualiza un préstamo en la base de datos."""
        pass
    @abstractmethod
    def get_by_id(self, loan_id: UUID) -> Loan:
        """Busca un préstamo por ID."""
        pass
    # Para el caso de uso return_loan
    @abstractmethod
    def mark_returned(self, loan: Loan) -> Loan:
        """Marca un préstamo como 'returned'."""
        pass