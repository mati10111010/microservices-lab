from src.domain.entities.loan import Loan
from src.domain.rules.loan_validator import LoanValidator
from src.application.dtos.loan_request_dto import CreateLoanRequestDTO
from src.application.dtos.loan_response_dto import LoanResponseDTO
from typing import TYPE_CHECKING

# Importaciones de Puertos (Interfaces)
if TYPE_CHECKING:
    from src.domain.ports.loan_repo import LoanRepository
    from src.domain.ports.books_repo import BooksRepository
    from src.domain.ports.clock import Clock
    from src.domain.ports.uuid_gen import UUIDGenerator
class CreateLoanUC:
    """Caso de Uso: Crear un nuevo préstamo.
    Orquesta la validación de reglas y el guardado en la base de datos."""
    def __init__(self, 
                 loan_validator: LoanValidator,
                 loan_repo: 'LoanRepository',
                 books_repo: 'BooksRepository',
                 clock: 'Clock',
                 uuid_gen: 'UUIDGenerator'):
        self.validator = loan_validator
        self.loan_repo = loan_repo
        self.books_repo = books_repo
        self.clock = clock
        self.uuid_gen = uuid_gen
    def execute(self, request: CreateLoanRequestDTO) -> LoanResponseDTO:
        """ 1. Ejecuta todas las reglas de negocio.
        2. Crea la Entidad Loan.
        3. Marca el libro como prestado (llamada externa).
        4. Persiste el préstamo.
        5. Retorna un DTO de respuesta."""
        # Validación de Reglas (Excepciones si falla)
        self.validator.validate_new_loan(
            user_id=request.user_id,
            book_id=request.book_id,
            due_date=request.due_date
        )
        # Creación de la Entidad Loan (Datos del Dominio)
        loan_id = self.uuid_gen.generate()
        loan_date = self.clock.get_current_date()
        new_loan = Loan(
            loan_id=loan_id,
            user_id=request.user_id,
            book_id=request.book_id,
            loan_date=loan_date,
            due_date=request.due_date,
        )

        # Marcar libro como prestado (Adaptador/Contrato)
        self.books_repo.mark_book_as_loaned(new_loan.book_id)

        # Persistir el préstamo (Adaptador/Contrato)
        self.loan_repo.save_loan(new_loan)

        # Retornar DTO
        return LoanResponseDTO(
            loan_id=new_loan.loan_id,
            user_id=new_loan.user_id,
            book_id=new_loan.book_id,
            loan_date=new_loan.loan_date,
            due_date=new_loan.due_date,
            status="active"
        )