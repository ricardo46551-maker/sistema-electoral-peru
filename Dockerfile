# 1. IMAGEN BASE: Usamos python 3.10-slim (Debian) para que apt-get funcione
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y permite ver los logs inmediatamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. INSTALAR CHROME: Bloque para instalar dependencias y Google Chrome Stable
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 3. DIRECTORIO DE TRABAJO
WORKDIR /app

# 4. DEPENDENCIAS PYTHON: Copiamos e instalamos los requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. CÓDIGO FUENTE: Copiamos el resto de tu aplicación
COPY . .

# 6. COMANDO DE INICIO:
# IMPORTANTE: Cambia "main.py" por el nombre de tu archivo principal (ej. app.py, index.py, etc.)
# Si usas Flask/Gunicorn, la línea sería algo como: CMD ["gunicorn", "app:app"]
CMD ["python", "app.py"]