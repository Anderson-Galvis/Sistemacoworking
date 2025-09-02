Coworking 

Sistema backend desarrollado con FastAPI y MySQL para la gestión de usuarios, salas y reservas en bloques de 1 hora.
Incluye autenticación JWT, roles (admin y user), validaciones de solapamiento de reservas y reportes básicos.

Instalación
1. Clonar el repositorio
git clone 


// crear e iniciar el entorno virtual 
pip install --user virtualenv

crear el entorno virtual 
~/.local/bin/virtualenv env

activar el entorno 
source env/bin/activate

// archivo con las dependencias 
//correr archivo requirements.txt 

pip install -r requirements.txt
// comando para correr unicorn
uvicorn app.main:app
