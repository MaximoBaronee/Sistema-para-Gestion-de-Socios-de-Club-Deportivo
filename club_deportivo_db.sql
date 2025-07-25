CREATE DATABASE; #Coloque el nombre de tu base de datos aquí
USE ; #Coloque el nombre de tu base de datos aquí 

-- Tabla de socios
CREATE TABLE socios (
    id_socio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dni VARCHAR(15) UNIQUE NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    email VARCHAR(100),
    tipo_membresia ENUM('Mensual', 'Trimestral', 'Anual') NOT NULL,
    estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de pagos
CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_socio INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha_pago DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado ENUM('Pagado', 'Pendiente', 'Vencido') DEFAULT 'Pendiente',
    FOREIGN KEY (id_socio) REFERENCES socios(id_socio) ON DELETE CASCADE
);

-- Tabla de usuarios del sistema (empleados)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave VARCHAR(255) NOT NULL,
    rol ENUM('Admin', 'Empleado') NOT NULL
);


DESC socios;


ALTER TABLE socios MODIFY telefono VARCHAR(20) NOT NULL;


SELECT * FROM socios;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM socios;
ALTER TABLE socios AUTO_INCREMENT = 1;
SET SQL_SAFE_UPDATES = 1;



