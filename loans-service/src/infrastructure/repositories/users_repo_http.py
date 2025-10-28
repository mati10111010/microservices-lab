import os
import requests
from requests.exceptions import Timeout, RequestException
from src.domain.ports.users_repo import UsersRepository

class UsersRepositoryHTTP(UsersRepository):
    """Adaptador HTTP para comunicarse con el Users-Service (Auth)."""

    def __init__(self):
        # Lee la URL base del entorno (variable de Docker Compose)
        self.base_url = os.environ.get('USERS_API_URL')
        self.timeout = 3 # Timeout de 3 segundos
        self.max_retries = 2 # Máximo 2 reintentos
        
    def _make_request_with_retry(self, url):
        """Lógica para peticiones GET."""
        for attempt in range(self.max_retries + 1):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status() # Lanza error para códigos 4xx/5xx
                return response.json()
            except Timeout:
                if attempt >= self.max_retries:
                    raise RequestException(f"API de Usuarios no responde, {self.max_retries} reintentos.")
            except RequestException as e:
                # Manejo de fallos de red o 4xx/5xx
                if attempt >= self.max_retries:
                    raise RequestException(f"Fallo al contactar Users-Service: {e}")
            
    def get_user_status(self, user_id: int):
        url = f"{self.base_url}/api/users/{user_id}"
        return self._make_request_with_retry(url)

    def get_active_loans_count(self, user_id: int):
        url = f"{self.base_url}/api/users/{user_id}/loans/count?status=active"
        data = self._make_request_with_retry(url)
        # Asumimos que el contrato retorna { count: number }
        return data.get('count', 0)