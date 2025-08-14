FROM python:3.10-alpine

RUN apk add --no-cache openjdk11 wget ca-certificates \
    gcc musl-dev python3-dev linux-headers fontconfig ttf-dejavu bash coreutils \
    git texlive-xetex

# Variables de entorno para Spark y Java
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk" \
    SPARK_VERSION="3.5.0" \
    HADOOP_VERSION="3"  \
    PYSPARK_PYTHON="/usr/bin/python3"

RUN mkdir -p "${SPARK_HOME}/jars"

RUN wget "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    tar xf "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" && \
    mv "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}" /opt/spark && \
    rm "spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz"

ENV MYSQL_CONNECTOR_VERSION="8.0.33"
RUN wget "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/${MYSQL_CONNECTOR_VERSION}/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar" -O "${SPARK_HOME}/jars/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar" \
    && ls -lh "${SPARK_HOME}/jars/" # Verificar que el JAR fue descargado

ENV SPARK_HOME="/opt/spark" \
    PATH="$PATH:/opt/spark/bin:/opt/spark/sbin" \
    PYTHONPATH="$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip"

RUN pip install --no-cache-dir pyspark findspark pandas jupyter mysql-connector-python

WORKDIR /workspace

# Comando para mantener el contenedor en ejecución
CMD ["sleep", "infinity"]