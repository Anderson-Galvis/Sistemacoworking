agregamos el archivo para ignorar la subida de las cosas importantes .gitignore

creamos archivo requeriments.txt para las dependencias que necesitaremos 

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
