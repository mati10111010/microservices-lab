import httpx
from httpx import ConnectTimeout, ReadTimeout
from ...domain.ports.users_repo import UsersRepository
from ...domain.rules.validators import DomainException
from typing import Dict, Any
# Configuración de resiliencia [cite: 203]
TIMEOUT = 3.0  # Segundos [cite: 203]
MAX_RETRIES = 2 # Máximo 2 reintentos [cite: 203]
class UsersRepositoryHTTP(UsersRepository):
    def __init__(self, base_url: str):
        self._base_url = base_url
    def _make_request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self._base_url}{path}"
        for attempt in range(MAX_RETRIES + 1):
            try:
                # Simulación de la llamada HTTP con manejo de timeout 
                response = httpx.request(method, url, timeout=TIMEOUT, **kwargs)
                response.raise_for_status()
                return response.json()
            except (ConnectTimeout, ReadTimeout) as e:
                if attempt == MAX_RETRIES:
                    raise DomainException(f"Users Service timeout: {e}")
                # Loggear reintento...
            except httpx.HTTPStatusError as e:
                # Mapeo de errores HTTP a errores de dominio [cite: 263]
                if e.response.status_code in [404, 400]:
                    raise DomainException(f"Users Service error (4xx): {e}")
                if e.response.status_code >= 500:
                    raise DomainException(f"Users Service error (5xx): {e}")
        return {} # Nunca debería llegar aquí
    # Contrato: GET /api/users/{id} → { id, email, status: "active"|"suspended" } [cite: 199]
    def get_user_status(self, user_id: str) -> str:
        data = self._make_request("GET", f"/api/users/{user_id}")
        return data.get("status", "not_found")
    # Contrato: GET /api/users/{id}/loans/count?status=active → { count: number } [cite: 199]
    def count_active_loans(self, user_id: str) -> int:
        data = self._make_request("GET", f"/api/users/{user_id}/loans/count?status=active")
        return data.get("count", 0)