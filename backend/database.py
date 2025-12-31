import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "club_deportivo_db")
}

def conectar_db():
    """Establece la conexión con la base de datos."""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def ejecutar_consulta(query, valores=None, fetch=False):
    """Ejecuta una consulta en la base de datos."""
    conexion = conectar_db()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor()
        if valores:
            cursor.execute(query, valores)
        else:
            cursor.execute(query)
        if fetch:
            resultados = cursor.fetchall()
            return resultados
        conexion.commit()
    except mysql.connector.Error as e:
        print(f"Error en la consulta: {e}")
    finally:
        cursor.close()
        conexion.close()
    return None