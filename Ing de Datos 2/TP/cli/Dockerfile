FROM python:3.11-slim

WORKDIR /app

# Instalamos herramientas mínimas y la librería 'rich' para el TUI
RUN apt-get update && apt-get install -y \
    curl \
    # CORRECCIÓN: Usar el paquete compatible que proporciona el cliente 'mysql'
    default-mysql-client \
    netcat-openbsd \
    vim \
    wget \
    gnupg \
    # -------------------------------------------------------------------
    # 1. SETUP DE MONGOSH
    # -------------------------------------------------------------------
    && curl -fsSL https://pgp.mongodb.com/server-8.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-8.0.gpg \
    && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/8.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list \
    && apt-get update \
    && apt-get install -y mongodb-mongosh \
    \
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