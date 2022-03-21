from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server_helper import *
from clases import *

app = FastAPI()

# Esto es porque el back corre en una URL distinta que el front en las pruebas y 
# el navegador se queja sino de que las urls no corresponden
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}") # http://localhost:8000/items/1?q=kk
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

#El metodo do-create que el AccountService del front tiene que llamar (te mete un usuario)
#http://localhost:8000/docs/    <- para debuguear puedes hacer peticiones al backend (do-create), execute y ver en el response los detalles de que devuelve
@app.post("/do-create")
def do_create(user: User):
    #insertar en db imagen como blob?
    
    returnValue = registerUser(user)

    #respuesta del back al front
    return returnValue

@app.post("/do-login")
def do_login(email: str, password: str):
    #insertar en db imagen como blob?
    
    returnValue = loginUser({"email": email, "pwd": password})
    print(password,)
    #respuesta del back al front
    return returnValue

