import logging
import uuid
import mysql.connector 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError as MongoConnectionError 
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

# Importamos la configuración centralizada
from db_config import DB_CONFIG

logger = logging.getLogger(__name__)

class CatTrackDBManager:
    """
    Clase para gestionar conexiones, esquemas y operaciones CRUD en
    MySQL (perfiles), MongoDB (eventos) y Cassandra (ubicaciones).
    """
    def __init__(self):
        self.config = DB_CONFIG
        self.mysql_conn = None
        self.mongo_client = None
        self.cassandra_session = None

    # =========================================================================
    #                  MÉTODOS DE CONEXIÓN Y ESQUEMA
    # =========================================================================

    def connect_all(self):
        """Intenta conectar a las tres bases de datos e inicializar esquemas."""
        
        mysql_ok = self._connect_mysql()
        mongo_ok = self._connect_mongodb()
        cassandra_ok = self._connect_cassandra()
        
        return mysql_ok and mongo_ok and cassandra_ok

    def _connect_mysql(self):
        """Conecta a MySQL y asegura que la base de datos y el esquema existan."""
        try:
            # Conexión inicial (sin DB específica) para crear la DB si no existe
            conn = mysql.connector.connect(
                host=self.config["mysql"]["host"],
                user=self.config["mysql"]["user"],
                password=self.config["mysql"]["password"],
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()
            db_name = self.config["mysql"]["database"]
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cursor.close()
            conn.close()

            # Reconectar con la base de datos creada y verificar la tabla
            self.mysql_conn = mysql.connector.connect(
                host=self.config["mysql"]["host"],
                user=self.config["mysql"]["user"],
                password=self.config["mysql"]["password"],
                database=db_name,
                auth_plugin='mysql_native_password'
            )
            logger.info("Conexión a MySQL exitosa.")
            self._setup_mysql_schema()
            return True
        except Exception as e:
            logger.error(f"Error al conectar o inicializar MySQL: {e}")
            self.mysql_conn = None
            return False

    def _setup_mysql_schema(self):
        """
        Crea la tabla de perfiles de gatos en MySQL.
        IMPORTANTE: Se añade DROP TABLE para forzar la actualización del esquema 
        (ej: añadir 'breed' y 'age_years') en entorno de desarrollo.
        """
        if not self.mysql_conn: return
        cursor = self.mysql_conn.cursor()
        
        # FIX 1: Eliminar tabla para asegurar que las columnas existan
        cursor.execute("DROP TABLE IF EXISTS cat_profiles")
        
        create_table_query = """
        CREATE TABLE cat_profiles ( 
            cat_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            breed VARCHAR(100),
            age_years INT
        )
        """
        cursor.execute(create_table_query)
        self.mysql_conn.commit()
        cursor.close()
        logger.info("Esquema de MySQL (cat_profiles) verificado/creado.")

    def _connect_mongodb(self):
        """Conecta a MongoDB con autenticación."""
        try:
            # FIX 2: Añadir usuario y contraseña para autenticación
            self.mongo_client = MongoClient(
                self.config["mongodb"]["uri"], 
                username=self.config["mongodb"]["user"],
                password=self.config["mongodb"]["password"],
                authSource='admin', # Usa la base de datos 'admin' para la autenticación de root
                serverSelectionTimeoutMS=5000
            )
            self.mongo_client.server_info() 
            logger.info("Conexión a MongoDB exitosa.")
            return True
        except MongoConnectionError as e:
            logger.error(f"Error al conectar a MongoDB: {e}")
            self.mongo_client = None
            return False
        except Exception as e:
            logger.error(f"Error inesperado al conectar a MongoDB: {e}")
            self.mongo_client = None
            return False

    def _connect_cassandra(self):
        """Conecta a Cassandra y asegura que el keyspace y la tabla existan."""
        try:
            cluster = Cluster(self.config["cassandra"]["hosts"], port=self.config["cassandra"]["port"])
            session = cluster.connect()
            
            keyspace = self.config["cassandra"]["keyspace"]
            
            # FIX 3: Eliminar Keyspace para forzar la recreación de la tabla con la columna 'y_coord'
            session.execute(f"DROP KEYSPACE IF EXISTS {keyspace}")

            # Crear Keyspace si no existe
            session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {keyspace}
                WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
            """)
            
            session.set_keyspace(keyspace)
            session.row_factory = dict_factory 
            
            # Tabla de ubicaciones (Time-Series)
            session.execute("""
                CREATE TABLE IF NOT EXISTS cat_locations (
                    cat_id text,
                    timestamp timeuuid,
                    x_coord float,
                    y_coord float,
                    PRIMARY KEY ((cat_id), timestamp)
                ) WITH CLUSTERING ORDER BY (timestamp DESC)
            """)
            
            self.cassandra_session = session
            logger.info("Conexión a Cassandra exitosa. Keyspace y tabla verificados.")
            return True
        except Exception as e:
            logger.error(f"Error al conectar o inicializar Cassandra: {e}")
            self.cassandra_session = None
            return False

    def close_all(self):
        """Cierra todas las conexiones activas."""
        if self.mysql_conn:
            self.mysql_conn.close()
            logger.info("Conexión MySQL cerrada.")
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("Conexión MongoDB cerrada.")
        if self.cassandra_session:
            self.cassandra_session.shutdown()
            logger.info("Conexión Cassandra cerrada.")
    
    # =========================================================================
    #                         MÉTODOS CRUD IMPLEMENTADOS
    # =========================================================================

    def insert_or_update_mysql_profile(self, cat_id, name, breed, age_years):
        """Inserta o actualiza un perfil de gato en MySQL."""
        if not self.mysql_conn: return
        try:
            cursor = self.mysql_conn.cursor()
            query = """
            INSERT INTO cat_profiles (cat_id, name, breed, age_years) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=%s, breed=%s, age_years=%s
            """
            data = (cat_id, name, breed, age_years, name, breed, age_years)
            cursor.execute(query, data)
            self.mysql_conn.commit()
            logger.info(f"MySQL: Perfil de gato '{name}' insertado/actualizado.")
        except Exception as e:
            # Cambiamos a logger.info ya que el error de columna se maneja con DROP/CREATE
            logger.info(f"MySQL: Error al insertar/actualizar perfil: {e}") 

    def get_mysql_profile(self, cat_id):
        """Obtiene un perfil de gato por ID de MySQL."""
        if not self.mysql_conn: return
        try:
            cursor = self.mysql_conn.cursor(dictionary=True)
            query = "SELECT cat_id, name, breed, age_years FROM cat_profiles WHERE cat_id = %s"
            cursor.execute(query, (cat_id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            logger.info(f"MySQL: Error al leer perfil: {e}")
            return None

    def insert_mongodb_event(self, cat_id, event_type, details):
        """Inserta un evento de comportamiento en MongoDB."""
        if not self.mongo_client: return
        try:
            db = self.mongo_client[self.config["mongodb"]["database"]]
            collection = db[self.config["mongodb"]["collection"]]
            
            document = {
                "cat_id": cat_id,
                "timestamp": str(uuid.uuid4()), # Identificador único para el evento
                "event_type": event_type,
                "details": details
            }
            collection.insert_one(document)
            logger.info(f"MongoDB: Evento '{event_type}' para {cat_id} insertado.")
        except Exception as e:
            logger.info(f"MongoDB: Error al insertar evento: {e}")

    def get_mongodb_recent_events(self, cat_id, limit=3):
        """Obtiene los eventos recientes de un gato desde MongoDB."""
        if not self.mongo_client: return
        try:
            db = self.mongo_client[self.config["mongodb"]["database"]]
            collection = db[self.config["mongodb"]["collection"]]
            
            # Ordena por _id (timestamp implícito) de forma descendente
            results = collection.find({"cat_id": cat_id}).sort("_id", -1).limit(limit)
            return list(results)
        except Exception as e:
            logger.info(f"MongoDB: Error al leer eventos: {e}")
            return []

    def insert_cassandra_location(self, cat_id, x_coord, y_coord):
        """Inserta una coordenada de ubicación para el gato en Cassandra."""
        if not self.cassandra_session: return
        try:
            query = """
            INSERT INTO cat_locations (cat_id, timestamp, x_coord, y_coord)
            VALUES (%s, now(), %s, %s)
            """
            self.cassandra_session.execute(query, (cat_id, x_coord, y_coord))
            logger.info(f"Cassandra: Ubicación para {cat_id} ({x_coord}, {y_coord}) insertada.")
        except Exception as e:
            logger.info(f"Cassandra: Error al insertar ubicación: {e}")

    def get_cassandra_latest_location(self, cat_id):
        """Obtiene la última ubicación registrada de un gato desde Cassandra."""
        if not self.cassandra_session: return
        try:
            query = """
            SELECT cat_id, toTimestamp(timestamp) as time, x_coord, y_coord 
            FROM cat_locations 
            WHERE cat_id = %s 
            LIMIT 1
            """
            result = self.cassandra_session.execute(query, (cat_id,)).one()
            return result
        except Exception as e:
            logger.info(f"Cassandra: Error al leer ubicación: {e}")
            return None
