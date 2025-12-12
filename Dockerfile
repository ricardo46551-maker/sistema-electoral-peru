# Usamos una base de Python ligera
FROM python:3.11-slim

# 1. Instalar Google Chrome y dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# 2. Configurar variables de entorno para que tu código encuentre Chrome
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PORT=8501

# 3. Preparar la carpeta de trabajo
WORKDIR /app
COPY . .

# 4. Instalar tus librerías (Streamlit, Selenium, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Comando para encender la app
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0