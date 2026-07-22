# 1. Utilizar un sistema operativo Linux muy ligero con Python preinstalado
FROM python:3.12-slim

# 2. Definir la carpeta de trabajo dentro del contenedor
WORKDIR /workspace

# 3. Instalar librerías del sistema necesarias para compilar dependencias (como FAISS)
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# 4. Copiar los archivos de configuración
COPY requirements.txt .
COPY start.sh .

# 5. Otorgar permisos de ejecución al script de arranque
RUN chmod +x start.sh

# 6. Instalar las dependencias de Python de Nigredo
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copiar el código fuente, la base vectorial, recursos e identidad visual
COPY app/ app/
COPY data/ data/
COPY pictures/ pictures/
COPY faiss_index/ faiss_index/
RUN mv app/.streamlit .streamlit
COPY .env .env

# 8. Abrir los puertos de comunicación
EXPOSE 8000
EXPOSE 8501

# 9. Ejecutar el ecosistema completo
CMD ["./start.sh"]
