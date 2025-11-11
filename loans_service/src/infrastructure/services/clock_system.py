from datetime import date
from ...domain.ports.clock import Clock
class SystemClock(Clock):
    """Implementación real del puerto Clock usando la hora del sistema."""
    def get_current_date(self) -> date:
        return date.today()