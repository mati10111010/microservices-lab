from datetime import date
from src.domain.ports.clock import Clock 
# Asume que Clock ya fue definido como ABC

class SystemClock(Clock):
    """Adaptador de infraestructura que usa la fecha actual del sistema."""
    def get_current_date(self) -> date:
        return date.today()