from dependency_injector import containers, providers
from datetime import date
from uuid import UUID

# Puertos
from ...domain.ports.users_repo import UsersRepository
from ...domain.ports.books_repo import BooksRepository
from ...domain.ports.loans_repo import LoansRepository
from ...domain.ports.clock import Clock
from ...domain.ports.uuid_gen import UUIDGenerator
# Adaptadores
from ..services.uuid_native import NativeUUIDGenerator
from ..services.clock_system import SystemClock
from ..repositories.users_repo_http import UsersRepositoryHTTP
from ..repositories.books_repo_http import BooksRepositoryHTTP
# Lógica de Dominio y Aplicación
from ...domain.rules.validators import LoanValidator
from ...domain.services.loan_service import LoanService
from ...application.use_cases.create_loan_uc import CreateLoanUseCase

# Adaptador de persistencia de Django (simulado, requiere setup de Django)
class LoansRepositoryDjango(LoansRepository):
    def save(self, loan):
        # Lógica ORM de Django (simulado)
        # LoanModel.objects.create(id=loan.id, ...)
        print(f"DEBUG: Persistiendo Loan {loan.id} con Django ORM...")
        return loan
    def get_by_id(self, loan_id):
        # Lógica ORM de Django (simulado)
        # return LoanModel.objects.get(id=loan_id)
        print(f"DEBUG: Obteniendo Loan {loan_id} con Django ORM...")
        # Devolvemos un mock para la demo como un diccionario simple
        return {
            "id": loan_id,
            "user_id": "user-123",
            "book_id": "book-456",
            "start_date": date.today(),
            "due_date": date.today().replace(day=date.today().day + 15),
            "status": "active",
        }    
    def mark_returned(self, loan):
        # Lógica ORM de Django para actualizar
        print(f"DEBUG: Marcando Loan {loan.id} como returned...")
        return loan


class Container(containers.DeclarativeContainer):
    """Contenedor de Inyección de Dependencias (DI)."""
    # Configuraciones (URLs de otros servicios)
    config = providers.Configuration()
    # Adaptadores Básicos (Implementaciones de Puertos) ---
    uuid_gen = providers.Singleton(NativeUUIDGenerator)
    clock = providers.Singleton(SystemClock)
    # Adaptadores de Repositorio (Infraestructura) ---
    # HTTP Repositories
    users_repo = providers.Singleton(
        UsersRepositoryHTTP,
        base_url=config.users_service_url,
    )
    books_repo = providers.Singleton(
        BooksRepositoryHTTP,
        base_url=config.books_service_url,
    )
    # Django ORM Repository
    loans_repo = providers.Singleton(LoansRepositoryDjango)
    # Dominio (Se inyectan dependencias) ---
    loan_validator = providers.Singleton(
        LoanValidator,
        users_repo=users_repo,
        books_repo=books_repo,
    )
    loan_service = providers.Singleton(
        LoanService,
        validator=loan_validator,
        loans_repo=loans_repo,
        books_repo=books_repo,
        clock=clock,
        uuid_gen=uuid_gen,
    )
    # Casos de Uso (Application) ---
    create_loan_uc = providers.Factory(
        CreateLoanUseCase,
        loan_service=loan_service,
    )