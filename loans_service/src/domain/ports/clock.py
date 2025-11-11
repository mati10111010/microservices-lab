from abc import ABC, abstractmethod
from datetime import date
class Clock(ABC):
    """Puerto para obtener la fecha y hora actual (facilita testing)."""
    @abstractmethod
    def get_current_date(self) -> date:
        pass