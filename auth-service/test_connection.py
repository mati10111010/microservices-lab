import os
import psycopg2
import redis
from time import sleep

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "main_db")
DB_USER = os.getenv("POSTGRES_USER", "devuser")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "devpass")
DB_PORT = os.getenv("DB_PORT", "5432")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# --- TEST DE CONEXIÓN A POSTGRESQL ---
def test_postgres_connection(max_retries=5):
    print(f"-> Intentando conectar a PostgreSQL en {DB_HOST}:{DB_PORT}...")
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                port=DB_PORT
            )
            conn.close()
            print("Conexión a PostgreSQL exitosa.")
            return True
        except psycopg2.Error as e:
            print(f"   [Intento {attempt + 1}/{max_retries}] Error de conexión a PostgreSQL: {e}")
            sleep(2) # Espera 2 segundos antes de reintentar
    print("Fallo en la conexión a PostgreSQL después de varios intentos.")
    return False

# --- TEST DE CONEXIÓN A REDIS ---
def test_redis_connection():
    print(f"\n-> Intentando conectar a Redis en {REDIS_HOST}:{REDIS_PORT}...")
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        r.ping()
        print("Conexión a Redis exitosa.")
        return True
    except redis.exceptions.ConnectionError as e:
        print(f"Fallo en la conexión a Redis: {e}")
        return False

if __name__ == "__main__":
    print("--- INICIANDO TEST DE CONEXIONES DE ENTORNO ---")
    
    # Este script requiere tener las librerías 'psycopg2-binary' y 'redis' instaladas.
    postgres_ok = test_postgres_connection()
    redis_ok = test_redis_connection()
    
    if postgres_ok and redis_ok:
        print("\n AMBAS CONEXIONES SON FUNCIONALES.")
    else:
        print("\n AL MENOS UNA CONEXIÓN FALLÓ.")