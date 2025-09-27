import os
import logging

# Configuración de Logging para toda la aplicación
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Silenciar los warnings de Cassandra para limpiar los logs en desarrollo
logging.getLogger('cassandra').setLevel(logging.ERROR)

# --- Configuración de Conexión (Obtenida de variables de entorno con valores por defecto) ---
DB_CONFIG = {
    "mysql": {
        "host": os.environ.get("MYSQL_HOST", "mysql"),
        "user": os.environ.get("MYSQL_USER", "root"),
        "password": os.environ.get("MYSQL_PASSWORD", "root_password"),
        "database": os.environ.get("MYSQL_DB", "cat_track_profiles")
    },
    "mongodb": {
        # El URI simple sigue siendo el host por defecto, pero ahora usamos usuario/pass para auth
        "uri": os.environ.get("MONGO_URI", "mongodb://mongodb:27017/"),
        "user": os.environ.get("MONGO_USER", "rootuser"),       # Agregado para autenticación
        "password": os.environ.get("MONGO_PASSWORD", "rootpassword"), # Agregado para autenticación
        "database": os.environ.get("MONGO_DB", "cat_track_events"),
        "collection": os.environ.get("MONGO_COLLECTION", "events")
    },
    "cassandra": {
        "hosts": os.environ.get("CASSANDRA_HOSTS", "cassandra").split(','),
        "port": int(os.environ.get("CASSANDRA_PORT", 9042)),
        "keyspace": os.environ.get("CASSANDRA_KEYSPACE", "cat_track_locations")
    }
}
