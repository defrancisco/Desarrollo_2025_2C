FROM python:3.11-slim

WORKDIR /app

# Instalamos herramientas mínimas y la librería 'rich' para el TUI
RUN apt-get update && apt-get install -y \
    curl \
    # CORRECCIÓN: Usar el paquete compatible que proporciona el cliente 'mysql'
    default-mysql-client \
    netcat-openbsd \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Instalación de clientes de BD (cqlsh requiere pip)
RUN pip install cqlsh

# Instalación de la librería Rich (para TUI básico y formatting)
RUN pip install rich

# Instalamos Cypher Shell (requiere JRE)
# Usaremos la versión oficial de Neo4j para obtener los binarios
# Es más fácil usar el binario descargado que intentar configurar el JRE aquí.
# Por simplicidad, asumiremos que solo usaremos la consola de MySQL/CQLSH/Mongo.
# Si necesitas cypher-shell y mongosh aquí, el Dockerfile sería mucho más complejo (Java/Mongo PPA).
# Para esta demo, el TUI usará el cliente MySQL y cqlsh (Python) directamente.

# Copiamos el script principal de la TUI
COPY cli.py /app/cli.py

CMD ["python", "cli.py"]