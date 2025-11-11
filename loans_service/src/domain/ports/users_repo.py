from abc import ABC, abstractmethod
from typing import Union
from uuid import UUID

class UsersRepository(ABC):
    """Puerto para obtener información de usuarios desde el User Service."""
    @abstractmethod
    def get_user_status(self, user_id: str) -> str:
        """Retorna el estado del usuario ('active', 'suspended', 'not_found')."""
        pass
    @abstractmethod
    def count_active_loans(self, user_id: str) -> int:
        """Retorna el número de préstamos activos que tiene el usuario."""
        pass