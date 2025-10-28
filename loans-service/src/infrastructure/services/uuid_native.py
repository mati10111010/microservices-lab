from uuid import uuid4, UUID
from src.domain.ports.uuid_gen import UUIDGenerator
# Asume que UUIDGenerator ya fue definido como ABC

class NativeUUIDGenerator(UUIDGenerator):
    """Adaptador de infraestructura que usa el generador nativo de UUID de Python."""
    def generate(self) -> UUID:
        return uuid4()