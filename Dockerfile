# Usamos imagen oficial de Python 3.12 slim
FROM python:3.12-slim

# Variables de entorno para evitar buffers en salida
ENV PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /app

# Copiar requirements.txt (crear este archivo con las dependencias)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Exponer el puerto que usa FastAPI (uvicorn)
EXPOSE 8000

# Comando para correr uvicorn con recarga automática
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
