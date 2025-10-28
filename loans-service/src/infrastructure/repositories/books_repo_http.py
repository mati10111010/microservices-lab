import os
import requests
from requests.exceptions import Timeout, RequestException
from src.domain.ports.books_repo import BooksRepository

class BooksRepositoryHTTP(BooksRepository):
    """Adaptador HTTP para comunicarse con el Books-Service."""

    def __init__(self):
        self.base_url = os.environ.get('BOOKS_API_URL')
        self.timeout = 3
        self.max_retries = 2

    def _make_request_with_retry(self, method, url):
        """Lógica de reintento para peticiones GET/POST."""
        for attempt in range(self.max_retries + 1):
            try:
                if method == 'GET':
                    response = requests.get(url, timeout=self.timeout)
                elif method == 'POST':
                    response = requests.post(url, timeout=self.timeout)

                response.raise_for_status()
                return response.json() if method == 'GET' else None # POSTs retornan 204/None
            except Timeout:
                if attempt >= self.max_retries:
                    raise RequestException(f"API de Libros no responde después de {self.max_retries} reintentos.")
            except RequestException as e:
                if attempt >= self.max_retries:
                    raise RequestException(f"Fallo al contactar Books-Service: {e}")
            
    def get_book_availability(self, book_id: int):
        url = f"{self.base_url}/api/books/{book_id}"
        return self._make_request_with_retry('GET', url)

    def mark_book_as_loaned(self, book_id: int):
        url = f"{self.base_url}/api/books/{book_id}/mark-loaned"
        self._make_request_with_retry('POST', url)

    def mark_book_as_returned(self, book_id: int):
        url = f"{self.base_url}/api/books/{book_id}/mark-returned"
        self._make_request_with_retry('POST', url)