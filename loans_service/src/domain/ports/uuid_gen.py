from abc import ABC, abstractmethod
from uuid import UUID

class UUIDGenerator(ABC):
    """Puerto para generar identificadores (facilita testing)."""

    @abstractmethod
    def generate(self) -> UUID:
        pass