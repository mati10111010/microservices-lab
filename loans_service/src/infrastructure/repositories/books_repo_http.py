import httpx
from ...domain.ports.books_repo import BooksRepository
from .users_repo_http import UsersRepositoryHTTP, TIMEOUT, MAX_RETRIES # Reutilizamos la lógica de retry/timeout
from ...domain.rules.validators import DomainException
class BooksRepositoryHTTP(BooksRepository):
    def __init__(self, base_url: str):
        self._base_url = base_url
        self._client = httpx.Client(timeout=TIMEOUT, base_url=base_url)
    # Contrato: GET /api/books/{id} → { id, title, status: "available"|"loaned"|"deleted" } [cite: 199]
    def get_book_status(self, book_id: str) -> str:
        try:
            response = self._client.get(f"/api/books/{book_id}")
            response.raise_for_status()
            return response.json().get("status", "not_found")
        except Exception as e:
            raise DomainException(f"Error al obtener estado del libro: {e}")
    # Contrato: POST /api/books/{id}/mark-loaned → 204 [cite: 199]
    def mark_loaned(self, book_id: str) -> None:
        try:
            response = self._client.post(f"/api/books/{book_id}/mark-loaned")
            response.raise_for_status()
        except Exception as e:
            raise DomainException(f"Error al marcar libro como prestado: {e}")