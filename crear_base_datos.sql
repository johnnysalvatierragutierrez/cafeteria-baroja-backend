-- Ejecuta esto en MySQL/MariaDB ANTES de arrancar Django
-- mysql -u root -p < crear_base_datos.sql

CREATE DATABASE IF NOT EXISTS cafeteria_baroja_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'cafeteria_user'@'localhost' IDENTIFIED BY 'cafeteria2024';
GRANT ALL PRIVILEGES ON cafeteria_baroja_db.* TO 'cafeteria_user'@'localhost';
FLUSH PRIVILEGES;

SELECT 'Base de datos cafeteria_baroja_db creada correctamente.' AS resultado;
