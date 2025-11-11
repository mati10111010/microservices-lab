# Usa una imagen base oficial de Python 3.11
FROM python:3.11
# Establece variables de entorno clave
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Define el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app/auth-service
# Copia solo el archivo de requisitos
COPY requirements.txt .
# Instala las dependencias (Este comando fallaba antes)
RUN pip install --no-cache-dir -r requirements.txt
# Copia todo el código fuente del proyecto (incluyendo manage.py)
# Ahora sí podemos usar COPY . . aquí, ya que está separado del RUN
COPY . .
# Expone el puerto por defecto de Django
EXPOSE 8000
