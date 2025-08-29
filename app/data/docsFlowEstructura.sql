-- Crear base de datos
CREATE DATABASE IF NOT EXISTS coworking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE coworking;

-- ===========================================
-- TABLA: Users
-- ===========================================
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    contraseña_hash VARCHAR(255) NOT NULL,
    rol ENUM('user','admin') DEFAULT 'user'
);

-- ===========================================
-- TABLA: Rooms
-- ===========================================
DROP TABLE IF EXISTS rooms;
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sede VARCHAR(100) NOT NULL,
    capacidad INT NOT NULL,
    recursos VARCHAR(255)
);

-- ===========================================
-- TABLA: Reservations
-- ===========================================
DROP TABLE IF EXISTS reservations;
CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    sala_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente',
    CONSTRAINT fk_reservation_user FOREIGN KEY (usuario_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_reservation_room FOREIGN KEY (sala_id) REFERENCES rooms(id) ON DELETE CASCADE
);