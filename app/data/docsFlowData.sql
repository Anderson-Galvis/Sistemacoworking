-- ===================================================
-- DATOS DE PRUEBA
-- ===================================================

-- Usuarios (contraseñas: Admin123 y User123)
-- hash generados con bcrypt (passlib)
INSERT INTO users (nombre, email, contraseña_hash, rol) VALUES
('Administrador', 'admin@local.com', '$2b$12$eIXqKZxOjv24Z/HQ7A4q1ezZ0p6N4spZ7n5zsw6F1/GZ1zF7RrTG6', 'admin'),
('Usuario Normal', 'user@local.com', '$2b$12$AWbF3o7XhH3sycCeB23JquC9v1q.2a9Ljg5bMGl06wAymvGkWlD7e', 'user');

-- Contraseña de admin@local.com = Admin123
-- Contraseña de user@local.com  = User123

-- Salas
INSERT INTO rooms (nombre, sede, capacidad, recursos) VALUES
('Sala Creativa', 'Sede Norte', 10, 'TV, Pizarra, Internet'),
('Sala Ejecutiva', 'Sede Centro', 20, 'Proyector, Aire Acondicionado'),
('Sala de Innovación', 'Sede Sur', 15, 'Pizarra, Internet');

-- Reservas de ejemplo (bloques de 1 hora exactos)
INSERT INTO reservations (usuario_id, sala_id, fecha, hora_inicio, hora_fin, estado) VALUES
(2, 1, '2025-09-02', '09:00:00', '10:00:00', 'confirmada'),
(2, 2, '2025-09-02', '11:00:00', '12:00:00', 'pendiente'),
(1, 3, '2025-09-03', '14:00:00', '15:00:00', 'confirmada');
