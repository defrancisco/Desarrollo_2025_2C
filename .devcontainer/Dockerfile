FROM python:3.10-slim-bullseye

# Instala las dependencias del sistema operativo y de mongosh
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    fontconfig \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    git \
    docker

# --- Agrega la clave GPG y el repositorio de MongoDB de la forma más confiable ---
# Descarga la clave GPG y la añade directamente a la lista de llaves de apt
RUN wget -qO- https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -

# Agrega el repositorio de MongoDB para Debian
RUN echo "deb http://repo.mongodb.org/apt/debian bullseye/mongodb-org/7.0 main" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Instala mongosh
# RUN apt-get update && apt-get install -y mongosh

# Instala las librerías de Python
# RUN pip install --no-cache-dir \
#     pandas \
#     jupyter \
#     mysql-connector-python \
#     pymongo

WORKDIR /workspace

# Comando para mantener el contenedor en ejecución
CMD ["sleep", "infinity"]