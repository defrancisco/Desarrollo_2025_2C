FROM python:3.10-slim-bullseye

# Instala las librerías de Python
RUN pip install --no-cache-dir \
    mysql-connector-python \
    pymongo\
    cassandra-driver

WORKDIR /workspace

# Comando para mantener el contenedor en ejecución
CMD ["sleep", "infinity"]