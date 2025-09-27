import logging
from db_initializer import CatTrackDBManager

logger = logging.getLogger(__name__)

def run_db_tests(db_manager):
    """Ejecuta las pruebas de conexión y reporta el estado."""
    
    print("\n" + "="*50)
    print(" INICIANDO PRUEBAS DE CONEXIÓN A BASES DE DATOS ")
    print("="*50)

    # El método connect_all intenta conectar e inicializar esquemas
    success = db_manager.connect_all()

    print("\n--- RESUMEN DE CONEXIONES Y ESQUEMA ---")
    print(f"MySQL (cat_profiles): {'[OK]' if db_manager.mysql_conn else '[FALLÓ]'} - Estructura verificada.")
    print(f"MongoDB (cat_track_events): {'[OK]' if db_manager.mongo_client else '[FALLÓ]'}")
    print(f"Cassandra (cat_track_locations): {'[OK]' if db_manager.cassandra_session else '[FALLÓ]'} - Keyspace y tabla verificados.")

    if success:
        print("\n¡Éxito! Todas las conexiones y esquemas están operativos.")
    else:
        print("\n¡Advertencia! Una o más conexiones fallaron. Revisa tus logs y configuración de Docker.")
        
    print("="*50)
    return success

def demonstrate_data_flow(db_manager, cat_id):
    """Demuestra la inserción y lectura de datos en las tres DBs."""
    
    print("\n" + "="*50)
    print(f" INICIANDO PRUEBAS DE FLUJO DE DATOS PARA {cat_id} ")
    print("="*50)

    # --- A. INSERTAR DATOS ---
    
    # MySQL: Insertar/Actualizar Perfil (Estructurado)
    db_manager.insert_or_update_mysql_profile(cat_id, "Mittens", "Siamese", 5)

    # MongoDB: Insertar Evento de Comportamiento (Flexible/Documento)
    db_manager.insert_mongodb_event(cat_id, "Siesta", {"duration_minutes": 60, "location": "sofa"})
    db_manager.insert_mongodb_event(cat_id, "Caza", {"target": "ratón de juguete", "success": True})

    # Cassandra: Insertar Ubicaciones (Time-Series)
    db_manager.insert_cassandra_location(cat_id, 10.5, 20.1)
    db_manager.insert_cassandra_location(cat_id, 10.6, 20.2)
    db_manager.insert_cassandra_location(cat_id, 10.7, 20.3)
    
    # --- B. LEER DATOS ---
    
    print("\n--- LECTURA DE DATOS ---")
    
    # MySQL: Leer Perfil
    profile = db_manager.get_mysql_profile(cat_id)
    logger.info(f"MySQL Perfil: {profile}")
    
    # MongoDB: Leer Eventos Recientes
    events = db_manager.get_mongodb_recent_events(cat_id)
    logger.info(f"MongoDB Eventos ({len(events)}): {[e['event_type'] for e in events]}")

    # Cassandra: Leer Última Ubicación
    location = db_manager.get_cassandra_latest_location(cat_id)
    
    # FIX 4: Añadir chequeo explícito para evitar TypeError: 'NoneType' object is not subscriptable
    if location:
        # toTimestamp() convierte el timeuuid en un timestamp legible
        time_str = location['time'].strftime('%H:%M:%S') if 'time' in location else 'N/A'
        logger.info(f"Cassandra Última Ubicación: X={location['x_coord']}, Y={location['y_coord']}, Time={time_str}")
    else:
        logger.info("Cassandra Última Ubicación: No se pudieron leer datos o ocurrió un error.")
    
    print("="*50)


if __name__ == "__main__":
    db_manager = CatTrackDBManager()
    
    try:
        if run_db_tests(db_manager):
            # Si las conexiones fueron exitosas, procede con la demostración CRUD
            CAT_ID = "GATO_007"
            demonstrate_data_flow(db_manager, CAT_ID)
            
    finally:
        # Asegurarse de cerrar todas las conexiones al finalizar
        db_manager.close_all()
