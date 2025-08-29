-- ===========================================
-- DATOS DE PRUEBA
-- ===========================================

-- Usuarios de prueba (contraseña real = '123456' encriptada con bcrypt)
INSERT INTO users (nombre, email, contraseña_hash, rol) VALUES
('Admin Principal', 'admin@coworking.com', '$2b$12$C6UzMDM.H6dfI/f/IKxGhu4zD8Kf6r5GtQYBZtWpoKn1yX0j8Vd5K', 'admin'),
('Juan Pérez', 'juan@correo.com', '$2b$12$C6UzMDM.H6dfI/f/IKxGhu4zD8Kf6r5GtQYBZtWpoKn1yX0j8Vd5K', 'user'),
('María Gómez', 'maria@correo.com', '$2b$12$C6UzMDM.H6dfI/f/IKxGhu4zD8Kf6r5GtQYBZtWpoKn1yX0j8Vd5K', 'user');

-- Salas de prueba
INSERT INTO rooms (nombre, sede, capacidad, recursos) VALUES
('Sala Innovación', 'Bogotá', 10, 'pizarra,proyector'),
('Sala Creativa', 'Medellín', 6, 'pantalla,tv'),
('Sala Ejecutiva', 'Bogotá', 12, 'pizarra,teleconferencia');

-- Reservas de prueba
INSERT INTO reservations (usuario_id, sala_id, fecha, hora_inicio, hora_fin, estado) VALUES
(2, 1, '2025-09-01', '09:00:00', '10:00:00', 'confirmada'),
(3, 2, '2025-09-01', '11:00:00', '12:00:00', 'confirmada'),
(2, 3, '2025-09-02', '14:00:00', '15:00:00', 'pendiente');