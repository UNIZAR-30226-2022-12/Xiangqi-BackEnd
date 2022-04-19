from datetime import timedelta
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

@app.post("/do-create")
def do_create(data: User):
    returnValue = registerUser(data)
    return returnValue

@app.post("/do-login")
def do_login(data: LoginData):
    returnValue = loginUser(data)
    return returnValue

@app.get("/do-getProfile/{id}")
#def do_getProfile(id: int, id2: int):
def do_getProfile(id: int, id2: int = Depends(verify_token)):
    returnValue = perfil(id)
    return returnValue

@app.post("/do-validate")
def do_validate(data: EmailData):
    exist = validate(data)
    return exist

@app.post("/do-forgotPwd")
def do_forgotPwd(data: EmailData):   
    exist = forgotPwd(data.email)
    return exist

@app.post("/do-changePwd")
def do_changePwd(data : LoginData):  
    returnValue = changePwd(data)
    return returnValue

@app.get("/do-getCountries")
def do_getCountries():
    returnValue = getAllCountries()
    return returnValue

@app.get("/do-getProfileImage/{id}")
#def do_getProfileImage(id: int ,id2: int):
def do_getProfileImage(id: int, id2: int = Depends(verify_token)):
    exito, image = getUserImage(id)
    if exito: 
        return image
    else:
        return {"error": False}

@app.post("/do-changeProfile/{nickname}/{name}/{date}/{country}/{pwd}")
#def do_changeProfile(nickname: str, name: str, date: str, country: str, pwd: str, image: Image, id: int):
def do_changeProfile(nickname: str, name: str, date: str, country: str, pwd: str, image: Image, id: int = Depends(verify_token)):
    user = {'nickname': nickname, 
            'name': name, 
            'date': date, 
            'country': country, 
            'pwd': pwd}
    exito = editProfile(id, user, image.image)
    return exito

@app.get("/do-deleteAccount")
#def do_deleteAccount(id: int):
def do_deleteAccount(id: int = Depends(verify_token)):
    exito = deleteAccount(id)
    return exito

@app.get("/do-getRanking")
def do_getRanking(id: int):
#def do_getRanking(id: int = Depends(verify_token)):
    ranking = getRanking()
    return ranking
    
@app.get("/do-getShopSkinList")
def do_getShopSkinList():
    skinList = getShopSkinList()
    return skinList
    
@app.get("/do-getUserSkinList/{id}")
def do_getUserSkinList(id: int):
    skinList = getUserSkinList(id)
    return skinList
    

