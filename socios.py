from database import ejecutar_consulta, conectar_db

def obtener_socios():
    """Recupera la lista de socios desde la base de datos."""
    query = "SELECT id_socio, nombre, dni, telefono, tipo_membresia, estado FROM socios"
    return ejecutar_consulta(query, fetch=True)

def agregar_socio(nombre, dni, telefono, tipo_membresia, estado):
    """Agrega un nuevo socio a la base de datos."""
    query = """INSERT INTO socios (nombre, dni, telefono, tipo_membresia, estado)
               VALUES (%s, %s, %s, %s, %s)"""
    valores = (nombre, dni, telefono, tipo_membresia, estado)
    return ejecutar_consulta(query, valores)

def eliminar_socio(id_socio):
    """Elimina un socio por su ID."""
    query = "DELETE FROM socios WHERE id_socio = %s"
    return ejecutar_consulta(query, (id_socio,))

def obtener_socios_con_pagos():
    """Obtiene la lista de socios con información de sus últimos pagos."""
    query = """
    SELECT s.id_socio, s.nombre, s.dni, 
           IFNULL((SELECT p.estado FROM pagos p 
                  WHERE p.id_socio = s.id_socio 
                  ORDER BY p.fecha_vencimiento DESC LIMIT 1), 'Pendiente') as estado_pago
    FROM socios s
    WHERE s.estado = 'Activo'
    """
    return ejecutar_consulta(query, fetch=True)

from database import ejecutar_consulta, conectar_db

def actualizar_estado_pago(id_socio, nuevo_estado):
    """Actualiza el estado de pago de manera confiable"""
    try:
        # Obtener tipo de membresía
        query_socio = "SELECT tipo_membresia FROM socios WHERE id_socio = %s"
        socio_data = ejecutar_consulta(query_socio, (id_socio,), fetch=True)
        
        if not socio_data:
            raise ValueError("Socio no encontrado")
        
        tipo_membresia = socio_data[0][0]
        
        # Calcular monto y período
        montos = {'Mensual': 3000, 'Trimestral': 8000, 'Anual': 25000}
        periodos = {'Mensual': 1, 'Trimestral': 3, 'Anual': 12}
        
        monto = montos.get(tipo_membresia, 0)
        meses = periodos.get(tipo_membresia, 1)
        
        # Insertar nuevo registro de pago
        query = """
        INSERT INTO pagos (id_socio, monto, fecha_pago, fecha_vencimiento, estado)
        VALUES (%s, %s, CURDATE(), DATE_ADD(CURDATE(), INTERVAL %s MONTH), %s)
        """
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(query, (id_socio, monto, meses, nuevo_estado))
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error en actualizar_estado_pago: {e}")
        if 'conexion' in locals():
            conexion.rollback()
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexion' in locals():
            conexion.close()