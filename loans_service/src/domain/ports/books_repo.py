from abc import ABC, abstractmethod
from typing import Union
from uuid import UUID
class BooksRepository(ABC):
    """Puerto para interactuar con el Book Service."""
    @abstractmethod
    def get_book_status(self, book_id: str) -> str:
        """Retorna el estado del libro ('available', 'loaned', 'deleted', 'not_found')."""
        pass
    @abstractmethod
    def mark_loaned(self, book_id: str) -> None:
        """Actualiza el estado del libro a 'loaned' en el Book Service."""
        pass