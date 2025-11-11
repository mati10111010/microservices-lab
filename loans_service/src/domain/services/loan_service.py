from datetime import date
from typing import TYPE_CHECKING, List
from uuid import UUID
from ..entities.loan import Loan
from ..rules.validators import LoanValidator
# Importaciones para type hinting (evitar ciclos)
if TYPE_CHECKING:
    from ..ports.users_repo import UsersRepository
    from ..ports.books_repo import BooksRepository
    from ..ports.loans_repo import LoansRepository
    from ..ports.clock import Clock
    from ..ports.uuid_gen import UUIDGenerator
    from ...application.dtos.loan_dto import LoanRequestDTO
class LoanService:
    def __init__(
        self,
        validator: LoanValidator,
        loans_repo: 'LoansRepository',
        books_repo: 'BooksRepository',
        clock: 'Clock',
        uuid_gen: 'UUIDGenerator',
    ):
        self._validator = validator
        self._loans_repo = loans_repo
        self._books_repo = books_repo
        self._clock = clock
        self._uuid_gen = uuid_gen
    def create_loan(self, request_dto: 'LoanRequestDTO') -> Loan:
        """Flujo para crear y validar un nuevo préstamo."""
        # Validar reglas de negocio (usando el validator que accede a puertos)
        self._validator.validate_new_loan(
            user_id=request_dto.user_id,
            book_id=request_dto.book_id,
            days=request_dto.days,
        )
        # Crear la entidad Loan
        new_loan = Loan.create(
            id=self._uuid_gen.generate(),
            user_id=request_dto.user_id,
            book_id=request_dto.book_id,
            start_date=self._clock.get_current_date(),
            days=request_dto.days,
        )
        # Persistir la entidad Loan
        persisted_loan = self._loans_repo.save(new_loan)
        # Notificar al Books Service que el libro ha sido prestado [cite: 199]
        self._books_repo.mark_loaned(request_dto.book_id)
        return persisted_loan
    def return_loan(self, loan_id: UUID) -> Loan:
        """Flujo para devolver un préstamo."""
        loan = self._loans_repo.get_by_id(loan_id)
        loan.status = "returned"
        self._loans_repo.mark_returned(loan)
        # Notificar al Books Service que el libro ha sido devuelto
        self._books_repo.mark_returned(loan.book_id)
        return loan