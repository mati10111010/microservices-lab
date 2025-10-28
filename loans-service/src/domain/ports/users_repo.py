from abc import ABC, abstractmethod
from typing import Dict, Any

class UsersRepository(ABC):
    """Puerto para consultar el estado de un usuario en el Servicio de Usuario(Auth)."""
    @abstractmethod
    def get_user_status(self, user_id: int) -> Dict[str, Any]:
        """
        Contrato: GET /api/users/{id}
        Retorna: { id, email, status: "active" | "suspended" }
        """
        pass
    
    @abstractmethod
    def get_active_loans_count(self, user_id: int) -> int:
        """
        Contrato: GET /api/users/{id}/loans/count?status=active
        Retorna: { count: number }
        """
        pass