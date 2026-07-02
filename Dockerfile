# ==============================
# ETAPA 1: Constructor (Builder)
# ==============================
FROM python:3.11-slim AS builder

WORKDIR /app

#Forzar buffer salida y evitar archivos .pyc en disco
ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#Herramientas de compilacion bascia por si fueran necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

#Copiar solo los requisitos para aprovechas la cache de capas de docker
COPY requirements.txt .

#Instalar dependencias en un directorio local asilado --user o pip
RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================
# ETAPA 2: Produccion /RunTime)"
# ==============================
FROM python:3.11-slim AS runner

WORKDIR /app

ENV PYTHONDONWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creamos un usuario y un grupo de sistemas sin privilegios non-root.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copiamos las dependencias de la etapa anterior
COPY --from=builder /root/.local /home/appuser/.local

# copiamos el código fuente de nuestra aplicación
COPY . .

# Cambiamos la propiedad de los archivos al usuario sin privilegios.
RUN chown -R appuser:appgroup /app 

# Aseguramos que el binario de ejecución esté en el path del nuevo usuario
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUSERBASE=/home/appuser/.local

# Exponemos el puerto y cambiamos al usuario seguro antes de arrancar.
USER appuser
EXPOSE 8000

CMD ["python", "main.py"]

