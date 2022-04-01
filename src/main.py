from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from server_helper import *
from clases import *

app = FastAPI()

def verify_token(request: Request):
    if 'x-access-token' not in request.headers: #busca la cabecera x-access-token en el request
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    token = request.headers['x-access-token']
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        #current_user = crud.get_user_by_uuid(db, data['public_id']) #obtener el usuario de la DB y devolverlo
        return data['id']
    except:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )   

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
def do_create(data: User):
    #insertar en db imagen como blob?
    
    returnValue = registerUser(data)

    #respuesta del back al front
    return returnValue

@app.post("/do-login")
def do_login(data: LoginData):
    #insertar en db imagen como blob?
    
    returnValue = loginUser(data)
    
    #respuesta del back al front
    return returnValue

@app.get("/do-getProfile/{id}")
def do_getProfile(id: int):
#def do_getProfile(id: int = Depends(verify_token)):
    #insertar en db imagen como blob?
    
    returnValue = perfil(id)
    print(returnValue)
    #respuesta del back al front
    return returnValue

@app.post("/do-validate")
def do_validate(data: EmailData):
    #insertar en db imagen como blob?
    
    exist = validate(data)
    #respuesta del back al front
    return exist

@app.post("/do-forgotPwd")
def do_forgotPwd(data: EmailData):
    #insertar en db imagen como blob?
    
    exist = forgotPwd(data.email)
    #respuesta del back al front
    return exist

@app.post("/do-changePwd")
def do_changePwd(data : LoginData):
    #insertar en db imagen como blob?
    
    returnValue = changePwd(data)
    #respuesta del back al front
    return returnValue

@app.get("/do-getCountries")
def do_getCountries():
    returnValue = allCountries()
    return returnValue


@app.get("/do-getProfileImage/{idDelOtro}/{id}")
#def do_getProfileImage(idDelOtro: int ,id: int):
def do_getProfileImage(idDelOtro: int ,id: int = Depends(verify_token)):
    #print("my id", id)
    exito, image = getUserImage(idDelOtro)

    #print(exito)
    if exito: 
        return image
    else:
        return {"error": "image not found"}

