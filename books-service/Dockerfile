# Usa la imagen base de Python
FROM python:3.11 
# Define el directorio de trabajo dentro del contenedor
WORKDIR /app
# Copia el archivo de dependencias e instala las librerías necesarias
COPY requirements.txt .
RUN pip install -r requirements.txt
# Indica el comando principal para iniciar el servidor de producción Gunicorn en el puerto 8000
COPY . .
CMD ["gunicorn", "auth_service.wsgi:application", "--bind", "0.0.0.0:8000"]
