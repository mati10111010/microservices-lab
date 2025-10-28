from datetime import date, timedelta
from typing import TYPE_CHECKING
from src.domain.exceptions import (
    MaxActiveLoansReachedError, InvalidLoanDurationError,
    UserNotActiveError, BookNotAvailableError
)
if TYPE_CHECKING:
    from src.domain.ports.loan_repo import LoanRepository
    from src.domain.ports.users_repo import UsersRepository
    from src.domain.ports.books_repo import BooksRepository
    from src.domain.ports.clock import Clock

class LoanValidator:
    """Reglas de negocio para la creación de un nuevo préstamo."""
    MAX_ACTIVE_LOANS = 3
    MAX_DAYS = 15
    
    def __init__(self, 
                 loan_repo: 'LoanRepository', 
                 users_repo: 'UsersRepository',
                 books_repo: 'BooksRepository',
                 clock: 'Clock'):
        self.loan_repo = loan_repo
        self.users_repo = users_repo
        self.books_repo = books_repo
        self.clock = clock

def validate_new_loan(self, user_id: int, book_id: int, due_date: date):
        """Ejecuta todas las validaciones."""
        self._check_user_status(user_id)        # Usuario activo
        self._check_max_active_loans(user_id)   # Máximo 3 préstamos
        self._check_loan_duration(due_date)     # Duración <= 15 días
        self._check_book_availability(book_id)  # Libro disponible

def _check_max_active_loans(self, user_id: int):
        """Regla: Máximo 3 préstamos activos por usuario."""
        # Usa el Puerto LoanRepository para consultar la DB
        active_loans_count = self.loan_repo.get_active_loans_count_by_user(user_id)
        
        if active_loans_count >= self.MAX_ACTIVE_LOANS:
            raise MaxActiveLoansReachedError(user_id)

def _check_loan_duration(self, due_date: date):
        """Regla: Duración <= 15 días."""
        # Usa el Puerto Clock para obtener la fecha actual
        loan_date = self.clock.get_current_date()
        
        max_allowed_date = loan_date + timedelta(days=self.MAX_DAYS)
        
        if due_date > max_allowed_date or due_date <= loan_date:
            raise InvalidLoanDurationError(self.MAX_DAYS)
            
def _check_user_status(self, user_id: int):
        """Usuario activo y no suspendido (Consulta Servicio de Usuario)."""
        # Usa el Puerto UsersRepository para consultar la API externa
        user_data = self.users_repo.get_user_status(user_id) 
        
        if user_data.get('status') != 'active':
            raise UserNotActiveError(user_id, user_data.get('status', ''))

def _check_book_availability(self, book_id: int):
        """Regla: Libro disponible (Consulta al Books-Service)."""
        # Usa el Puerto BooksRepository para consultar la API externa
        book_data = self.books_repo.get_book_availability(book_id)
        
        if not book_data.get('is_available'):
            reason = book_data.get('reason', 'Libro no encontrado o prestado.') 
            raise BookNotAvailableError(book_id, reason)