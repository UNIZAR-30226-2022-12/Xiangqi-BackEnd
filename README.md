# Xiangqi-BackEnd

database: ficheros para para la creacion y modificacion del BD
    run: python3 consulta.py

src/server: servidor de prueba, recibe peticion y usa server_helper para obtener returnValue
    run: python3 server.py

src/index.html: html de prueba, se lanza en localhost:8080, despues de lanza el servidor
    
src/db_helper.py: modulo para interactuar con BD

src/server_helper.py: modulo para obtener informacion a devolver de las peticiones

# Instalacion
### Instalar pip3
```
sudo apt install python3-pip
```
### Instalar dependencias
```
pip3 install -r requirements.txt
```
### lanzar uvicorn
```
uvicorn main:app --reload --host 0.0.0.0
```
### acceso a fastapi
```
localhost:8000/doc
```
