-- ===================================================
-- CREACIÓN DE BASE DE DATOS
-- ===================================================
DROP DATABASE IF EXISTS coworking_db;
CREATE DATABASE coworking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE coworking_db;

-- ===================================================
-- TABLA USERS
-- ===================================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    contraseña_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ===================================================
-- TABLA ROOMS
-- ===================================================
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL,
    recursos VARCHAR(500)
);

-- ===================================================
-- TABLA RESERVATIONS
-- ===================================================
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    sala_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado VARCHAR(30) DEFAULT 'pendiente',
    CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_sala FOREIGN KEY (sala_id) REFERENCES rooms(id) ON DELETE CASCADE
);
