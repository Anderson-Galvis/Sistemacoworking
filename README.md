Coworking 

Sistema backend desarrollado con FastAPI y MySQL para la gestión de usuarios, salas y reservas en bloques de 1 hora.
Incluye autenticación JWT, roles (admin y user), validaciones de solapamiento de reservas y reportes básicos.

Instalación
1. Clonar el repositorio
git clone https://github.com/Anderson-Galvis/Sistemacoworking.git

2. Crear y activar entorno virtual
// crear e iniciar el entorno virtual 
pip install --user virtualenv

crear el entorno virtual 
~/.local/bin/virtualenv env

activar el entorno 
source env/bin/activate

// archivo con las dependencias 
//correr archivo requirements.txt 


3. Instalar dependencias
pip install -r requirements.txt


// comando para correr unicorn
uvicorn app.main:app


4. Configurar variables de entorno 

5. Crear la base de datos y cargar datos de prueba

6. Ejecutar el servidor

 Tecnologías usadas
FastAPI
SQLAlchemy
MySQL
Passlib (bcrypt)
 → Hash de contraseñas
fastapi-jwt-auth
 → JWT