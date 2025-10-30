# setup/Dockerfile

# -------------------------------------------------------------------
# STAGE 1: Obtener el cliente Cypher Shell (cypher-shell-extractor)
# Usamos la imagen oficial de Neo4j para obtener el binario y sus librerías JAR de forma estable.
# -------------------------------------------------------------------
FROM neo4j:5-community AS cypher-shell-extractor

# -------------------------------------------------------------------
# STAGE 2: Construir la imagen final (setup_service)
# -------------------------------------------------------------------
FROM ubuntu:22.04 

# Definición de variables para MongoDB
ENV MONGO_VERSION 8.0
ENV UBUNTU_RELEASE focal

# -------------------------------------------------------------------
# INSTALACIÓN DE TODOS LOS CLIENTES Y HERRAMIENTAS
# -------------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # Paquetes estándar
    mysql-client \
    netcat-openbsd \
    curl \
    python3-pip \
    unzip \
    gnupg \
    wget \
    # -------------------------------------------------------------------
    # INSTALACIÓN CLAVE: Java Runtime Environment (JRE) para Cypher-Shell
    # -------------------------------------------------------------------
    && apt-get install -y software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y openjdk-17-jre \
    \
    # -------------------------------------------------------------------
    # 1. SETUP DE MONGOSH
    # -------------------------------------------------------------------
    && curl -fsSL https://pgp.mongodb.com/server-8.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-${MONGO_VERSION}.gpg \
    && echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-${MONGO_VERSION}.gpg ] https://repo.mongodb.org/apt/ubuntu ${UBUNTU_RELEASE}/mongodb-org/${MONGO_VERSION} multiverse" | tee /etc/apt/sources.list.d/mongodb-org-${MONGO_VERSION}.list \
    && apt-get update \
    && apt-get install -y mongodb-mongosh \
    \
    # -------------------------------------------------------------------
    # 2. INSTALACIÓN DE CLIENTES ADICIONALES (CQLSH)
    # -------------------------------------------------------------------
    && pip3 install cqlsh \
    \
    # -------------------------------------------------------------------
    # 3. LIMPIEZA FINAL
    # -------------------------------------------------------------------
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------
# COPIAR EL CLIENTE CYPHER SHELL (DESDE EL STAGE 1)
# Copiamos la estructura mínima requerida: binario y librerías (JARs).
# -------------------------------------------------------------------
# 1. Copiar binarios (incluye el script cypher-shell)
COPY --from=cypher-shell-extractor /var/lib/neo4j/bin /usr/local/neo4j-client/bin/
# 2. Copiar librerías (archivos JAR que contienen la clase CypherShellBoot)
COPY --from=cypher-shell-extractor /var/lib/neo4j/lib /usr/local/neo4j-client/lib/

# Crear el enlace simbólico (symlink) al PATH
RUN ln -s /usr/local/neo4j-client/bin/cypher-shell /usr/local/bin/cypher-shell
RUN chmod +x /usr/local/neo4j-client/bin/cypher-shell

# -------------------------------------------------------------------
# COPIAR SCRIPTS LOCALES (DEBEN EXISTIR EN LA CARPETA 'setup/')
# -------------------------------------------------------------------

# 1. Copiar wait-for-it.sh (El script de espera)
COPY wait-for-it.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-it.sh

# 2. Copiar init_all_dbs.sh (El script de orquestación)
COPY init_all_dbs.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/init_all_dbs.sh

# Entrypoint del contenedor
ENTRYPOINT ["/usr/local/bin/init_all_dbs.sh"]