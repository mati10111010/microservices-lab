from typing import TYPE_CHECKING
from ..dtos.loan_dto import LoanRequestDTO, LoanResponseDTO
if TYPE_CHECKING:
    from ...domain.services.loan_service import LoanService
class CreateLoanUseCase:
    def __init__(self, loan_service: 'LoanService'):
        self._loan_service = loan_service
    def execute(self, request_dto: LoanRequestDTO) -> LoanResponseDTO:
        # 1. Llama al servicio de dominio
        loan = self._loan_service.create_loan(request_dto)
        # 2. Mapea la Entidad de Dominio (Loan) a un DTO de respuesta
        return LoanResponseDTO(
            loan_id=loan.id,
            user_id=loan.user_id,
            book_id=loan.book_id,
            start_date=loan.start_date,
            due_date=loan.due_date,
            status=loan.status
        )