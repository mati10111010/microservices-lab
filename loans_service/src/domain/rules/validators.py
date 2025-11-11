# Excepciones de Dominio
class DomainException(Exception):
    pass
class UserInactiveException(DomainException):
    pass
class MaxLoansReachedException(DomainException):
    pass
class BookNotAvailableException(DomainException):
    pass
class LoanDurationException(DomainException):
    pass
# Reglas
MAX_LOANS = 3
MAX_DAYS = 15
class LoanValidator:
    def __init__(
        self,
        users_repo: 'UsersRepository',
        books_repo: 'BooksRepository',
    ):
        self._users_repo = users_repo
        self._books_repo = books_repo
    def validate_new_loan(self, user_id: str, book_id: str, days: int):
        """Valida todas las reglas de negocio antes de crear un préstamo."""
        # Regla: Duración <= 15 días [cite: 198]
        if days > MAX_DAYS:
            raise LoanDurationException(f"Duración máxima de {MAX_DAYS} días excedida.")
        # Regla: Usuario activo y no suspendido [cite: 198]
        user_status = self._users_repo.get_user_status(user_id)
        if user_status != "active":
            raise UserInactiveException(f"El usuario no está activo: {user_status}")
        # Regla: Máximo 3 préstamos activos por usuario [cite: 197]
        active_loans = self._users_repo.count_active_loans(user_id)
        if active_loans >= MAX_LOANS:
            raise MaxLoansReachedException(f"Máximo de {MAX_LOANS} préstamos activos alcanzado.")
        # Regla: Libro disponible (no eliminado, no 'prestado') [cite: 199]
        book_status = self._books_repo.get_book_status(book_id)
        if book_status != "available":
            raise BookNotAvailableException(f"El libro no está disponible: {book_status}")
# Importamos los puertos después para evitar importación circular
from ..ports.users_repo import UsersRepository
from ..ports.books_repo import BooksRepository