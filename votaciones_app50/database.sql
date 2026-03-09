CREATE DATABASE IF NOT EXISTS votaciones;

USE votaciones;

CREATE TABLE puestos_votacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_puesto VARCHAR(100),
    direccion VARCHAR(100)
);

CREATE TABLE ciudadanos (
    identificacion VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100),
    puesto_id INT,
    FOREIGN KEY (puesto_id) REFERENCES puestos_votacion(id)
);

INSERT INTO puestos_votacion (nombre_puesto, direccion) VALUES
('Colegio Central','Calle 10 #15-20'),
('Escuela Nacional','Carrera 8 #20-30'),
('Universidad Publica','Avenida 30 #45-10');