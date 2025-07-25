import mysql.connector

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "host": "", #Coloque la dirección de tu servidor de base de datos aquí,por ejemplo "localhost"
    "user": "", #Coloque el nombre de usuario de tu base de datos aquí,por ejemplo "root"
    "password": "", #Coloque la contraseña de tu base de datos aquí
    "database": "" #Coloque el nombre de tu base de datos aquí
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
