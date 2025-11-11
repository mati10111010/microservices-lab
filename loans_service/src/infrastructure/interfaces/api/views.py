from ...infrastructure.configs.container import Container
from rest_framework.views import APIView
from rest_framework.response import Response
from ...application.dtos.loan_dto import LoanRequestDTO # Asegúrate que la importación sea relativa y correcta
from django.conf import settings
from rest_framework import status

container = Container()
container.config.from_dict({
    "users_service_url": settings.USERS_SERVICE_URL,
    "books_service_url": settings.BOOKS_SERVICE_URL,
})
class CreateLoanAPIView(APIView):
    def post(self, request):
        try:
            # 2. Inyectar el Caso de Uso desde el contenedor
            create_loan_uc = container.create_loan_uc() 
            # 3. Mapear request.data a DTO
            request_dto = LoanRequestDTO(
                user_id=request.data['user_id'],
                book_id=request.data['book_id'],
                days=request.data['days']
            )
            # 4. Ejecutar el Caso de Uso (Dominio y Lógica Pura)
            response_dto = create_loan_uc.execute(request_dto)
            # 5. Retornar la respuesta HTTP
            return Response(response_dto.__dict__, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Manejo de excepciones de dominio y otros errores
            # Aquí deberías mapear las DomainException a respuestas HTTP 400
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)