from abc import ABC, abstractmethod
from typing import Dict, Any

class BooksRepository(ABC):
    """Puerto para consultar y actualizar el estado de un libro en el Books-Service."""

    @abstractmethod
    def get_book_availability(self, book_id: int) -> Dict[str, Any]:
        """
        Contrato: GET /api/books/{id}
        Retorna: { id, title, status: "available" | "loaned" | "deleted" }
        """
        pass

    @abstractmethod
    def mark_book_as_loaned(self, book_id: int):
        """Contrato: POST /api/books/{id}/mark-loaned (Retorna 204)"""
        pass

    @abstractmethod
    def mark_book_as_returned(self, book_id: int):
        """Contrato: POST /api/books/{id}/mark-returned (Retorna 204)"""
        pass