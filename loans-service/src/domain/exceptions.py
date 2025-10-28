class DomainException(Exception):
    """Eexcepciones del dominio."""
    pass
class MaxActiveLoansReachedError(DomainException):
    """El usuario alcanzo el límite máximo de préstamos activos (3)"""
    def __init__(self, user_id: int):
        super().__init__(f"El usuario {user_id} ya tiene el máximo.")
class InvalidLoanDurationError(DomainException):
    """El préstamo excede el límite permitido (15 días)."""
    def __init__(self, max_days: int):
        super().__init__(f"Excedes los {max_days} días.")
class UserNotActiveError(DomainException):
    """Usuario suspendido/no activo"""
    def __init__(self, user_id: int, status: str):
        super().__init__(f"El usuario {user_id} > Estado: {status}.")
class BookNotAvailableError(DomainException):
    """Libro no disponible para prestar"""
    def __init__(self, book_id: int, reason: str):
        super().__init__(f"Libro {book_id} no disponible. Razón: {reason}.")