from uuid import uuid4, UUID
from ...domain.ports.uuid_gen import UUIDGenerator
class NativeUUIDGenerator(UUIDGenerator):
    """Implementación real del puerto UUIDGenerator usando la librería nativa."""
    def generate(self) -> UUID:
        return uuid4()