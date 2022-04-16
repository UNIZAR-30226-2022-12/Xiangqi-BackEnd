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
### lanzar uvicorn local
```
uvicorn main:app --reload --host 0.0.0.0
```
### lanzar uvicorn maquina virtual
```
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```
### acceso a fastapi
```
http://localhost:3000/docs#/
```
### install aiofiles
```
pip install aiofiles 
```
### virtual server
```
ec2-3-82-235-243.compute-1.amazonawv.com
```
### instalar imageio
...

pip install imageio

...


